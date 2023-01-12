import os
from celery import Celery

# Set the standard Django settings for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ksu_project.settings')
app = Celery('ksu_project')

# We use the term so that the worker does not hide the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')
