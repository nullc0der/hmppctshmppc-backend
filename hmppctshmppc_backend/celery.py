import os
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'hmppctshmppc_backend.settings.production')

app = Celery('hmppctshmppc_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
