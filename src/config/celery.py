import os

from celery import Celery

from src.config.env import env


os.environ.setdefault(
    key='DJANGO_SETTINGS_MODULE',
    value=env('DJANGO_SETTINGS_MODULE')
)

celery = Celery('config')
celery.config_from_object('django.conf:django', namespace='CELERY')
celery.autodiscover_tasks()
