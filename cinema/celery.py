
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')

app = Celery('cinema')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

