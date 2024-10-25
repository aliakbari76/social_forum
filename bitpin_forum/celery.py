import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitpin_forum.settings')

app = Celery('bitpin_forum')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'calculate-total-distance-every-hour': {
        'task': 'core.tasks.process_all_unprocessed_votes',
        #'schedule': 20.0, #TODO switch it to every 2 hours ,  it will run every 20 seconds (for testing)
        'schedule': crontab(hour='*/2'),
    },
}
app.autodiscover_tasks()