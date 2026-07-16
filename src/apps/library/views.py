from rest_framework.viewsets import ModelViewSet
from apps.library.models import Author, Book, Borrowing
from apps.library.serializers import AuthorSerializer, \
    BookSerializer, BorrowingSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer


class BorrowingViewSet(ModelViewSet):
    queryset = Borrowing.objects.select_related('book__author')
    serializer_class = BorrowingSerializer

