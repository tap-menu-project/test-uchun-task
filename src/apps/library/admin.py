from django.contrib import admin
from apps.library.models import Author, Book, Borrowing

# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Borrowing)