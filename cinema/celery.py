import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')

app = Celery('cinema')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

from datetime import timedelta

app.conf.beat_schedule = {
    'send-top-films-email': {
        'task': 'apps.product.tasks.send_top_films_email',
        'schedule': timedelta(days=1),
    },
}
