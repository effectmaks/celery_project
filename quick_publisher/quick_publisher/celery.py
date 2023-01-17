# quick_publisher/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quick_publisher.settings')
app = Celery('quick_publisher')
app.config_from_object('django.conf:settings', namespace='CELERY_')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    # expires - истекает через 70 сек
    sender.add_periodic_task(30.0, test.s('world'), expires=70)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@app.task(name='run_settings_jobs')
def test_set():
    print("Print 10")

@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)


#https://code.tutsplus.com/ru/tutorials/using-celery-with-django-for-background-task-processing--cms-28732
#https://redis.io/docs/getting-started/installation/install-redis-on-windows/
