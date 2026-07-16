from rest_framework.viewsets import ModelViewSet
from apps.library.models import Author, Book, Borrowing
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.decorators import action
from django.db import transaction
from apps.library.serializers import AuthorSerializer, \
    BookSerializer, BorrowingSerializer
from apps.library.task import send_borrowing_confirmation, return_borrowing_confirmation


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = Book.objects.select_related('author')
        author_id_filter = self.request.query_params.get("author")
        if author_id_filter and author_id_filter.isnumeric():
            qs = qs.filter(author__id=author_id_filter)
        return qs


class BorrowingViewSet(ModelViewSet):
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        qs = Borrowing.objects.select_related("book__author")
        if self.request.query_params.get("active") == "true":
            qs = qs.filter(returned_at__isnull=True)
        return qs

    def perform_create(self, seralizer):
        with transaction.atomic():
            book = Book.objects.select_for_update().get(
                pk=seralizer.validated_data['book'].pk
            )
            if book.available_copies <= 0:
                raise ValidationError(
                    {"book_id": "No available copies for this book."}
                )
            book.available_copies -= 1
            book.save(update_fields=['available_copies'])
            seralizer.save()
            send_borrowing_confirmation(seralizer.instance.id)
        
    @action(detail=True, methods=['post'])
    def return_book(self, serializer=None, pk=None):
        with transaction.atomic():
            borrowing = self.get_object()
            if borrowing.returned_at is not None:
                raise ValidationError('This borrowing is already returned.')
            book = Book.objects.select_for_update().get(pk=borrowing.book_id)
            borrowing.returned_at = timezone.now().date()
            borrowing.save(update_fields=['returned_at'])
            book.available_copies += 1
            book.save(update_fields=['available_copies'])
            return_borrowing_confirmation(borrowing.id)
            return Response(self.get_serializer(borrowing).data,
                            status=status.HTTP_200_OK)

