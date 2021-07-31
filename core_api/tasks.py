from celery import shared_task

from core_api.utils import clean_access_token, create_stats_snapshot


@shared_task
def task_create_stats_snapshot(payment_id: str):
    return create_stats_snapshot(payment_id)


# NOTE: Test cleanup functions
@shared_task
def task_clean_access_token():
    return clean_access_token()
