from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, ValidationError
from apps.library.models import Author, Book, Borrowing
from django.utils import timezone

class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"
    
class BookSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id',
              'total_copies', 'available_copies', 'created_at']


class BorrowingSerializer(ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = PrimaryKeyRelatedField(
        queryset=Book.objects.select_related('author'),
        source='book',
        write_only=True
    )
    class Meta:
        model = Borrowing
        fields = ['id', 'book', 'book_id', 'borrower_name',
                  'borrowed_at', 'due_date', 'returned_at']
        read_only_fields = ['returned_at', 'borrowed_at']
    
    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise ValidationError("You don't borrow past days")
        return value
