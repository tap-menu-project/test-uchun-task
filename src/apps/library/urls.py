from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.library.views import AuthorViewSet, BookViewSet, \
    BorrowingViewSet

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="book")
router.register(r"borrowings", BorrowingViewSet, basename="borrowing")


urlpatterns = [
    path('', include(router.urls)),
]