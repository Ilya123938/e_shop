import os
from celery import Celery

# ضبط إعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# قراءة إعدادات Celery من settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# اكتشاف المهام من جميع التطبيقات
app.autodiscover_tasks()