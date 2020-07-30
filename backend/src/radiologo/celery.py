from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radiologo.settings')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://rd01:6379')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://rd01:6379'),

celery_app = Celery('radiologo', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'daily-alignment': {
        'task': 'programs.tasks.do_alignment',
        'schedule': crontab(minute='10', hour='06'),
    },
    'rss-upload': {
        'task': 'programs.tasks.upload_from_feed',
        'schedule': crontab(minute='10', hour='07')
    },
    'update-stats': {
        'task': 'programs.tasks.update_listener_stats',
        'schedule': crontab(minute='*/2')
    }
}
