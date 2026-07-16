from celery import shared_task
from apps.library.models import Borrowing
from django.utils import timezone

@shared_task
def send_borrowing_confirmation(borrowing_id):
    borrowing = Borrowing.objects.select_related('book').get(id=borrowing_id)
    print(f"[EMAIL] {borrowing.borrower_name}: "
          f"'{borrowing.book.title}' kitobi {borrowing.due_date}gacha ijarada.")

@shared_task
def return_borrowing_confirmation(borrowing_id):
    borrowing = Borrowing.objects.select_related('book').get(id=borrowing_id)
    print(f"[EMAIL] {borrowing.borrower_name}: "
          f"'{borrowing.book.title}' kitobi {borrowing.returned_at}da qaytarildi.")


@shared_task
def log_overdue_borrowings():
    overdue = Borrowing.objects.select_related('book').filter(
        due_date__lt=timezone.now().date(),
        returned_at__isnull=True
    )
    for b in overdue:
        print(f"[OVERDUE] {b.borrower_name}: '{b.book.title}' "
              f"muddati {b.due_date} da o'tgan, hali qaytarilmagan!")
    return f"{overdue.count()} ta muddati o'tgan ijara topildi"
