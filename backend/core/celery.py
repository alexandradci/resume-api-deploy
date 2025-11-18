from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from dotenv import load_dotenv


load_dotenv()

# Important: use backend.core.settings, not just core.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    from django.conf import settings
    pprint(f"DEBUG EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"DEBUG EMAIL_USER is set: {bool(settings.EMAIL_HOST_USER)}")
    print(f"Request: {self.request!r}")