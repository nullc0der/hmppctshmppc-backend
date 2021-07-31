from celery import shared_task

from payment_processor.utils import clean_unused_payments


@shared_task
def task_clean_unused_payments():
    return clean_unused_payments()
