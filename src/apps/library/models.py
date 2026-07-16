from django.db import models

# Create your models here.


class Author(models.Model):
    full_name = models.CharField(max_length=255)
    birth_year = models.PositiveSmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} | {self.birth_year}"


class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books")
    total_copies = models.PositiveIntegerField(default=0)
    available_copies = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} | {self.available_copies}"


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="borrowings")
    borrower_name = models.CharField(max_length=255)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} | {self.borrower_name}"
