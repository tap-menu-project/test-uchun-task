from celery import shared_task
from apps.library.models import Borrowing


@shared_task
def send_borrowing_confirmation(borrowing_id):
    borrowing = Borrowing.objects.select_related().get(id=borrowing_id)
    print(f"[EMAIL] {borrowing.borrower_name}: "
          f"'{borrowing.book.title}' kitobi {borrowing.due_date}gacha ijarada.")
