import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskly.settings')

celery = Celery('taskly')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
