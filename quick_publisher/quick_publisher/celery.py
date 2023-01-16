# quick_publisher/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quick_publisher.settings')
app = Celery('quick_publisher')
app.config_from_object('django.conf:settings', namespace='CELERY_')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

#https://code.tutsplus.com/ru/tutorials/using-celery-with-django-for-background-task-processing--cms-28732
#https://redis.io/docs/getting-started/installation/install-redis-on-windows/
