import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitterWatch.settings')

app = Celery('twitterWatch')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_twitter_trends': {
        'task': 'trends.tasks.get_twitter_trends',
        'schedule': crontab(minute='18', hour='*'),
        # toutes les heures (ex:12h18)  # https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
        # #crontab-schedules
    },
}
