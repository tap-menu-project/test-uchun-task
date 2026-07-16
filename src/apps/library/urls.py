from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.library.views import AuthorViewSet, BookViewSet, \
    BorrowingViewSet

router = DefaultRouter()
router.register(r"author", AuthorViewSet, basename="author")
router.register(r"book", BookViewSet, basename="book")
router.register(r"borrowing", BorrowingViewSet, basename="borrowing")


urlpatterns = [
    path('', include(router.urls)),
]