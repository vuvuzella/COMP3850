import os
from celery import Celery

# set the default Django settings module for the celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
        'runner_recommender_app.settings')
# os.environ.setdefault('DJANGO_CONFIGURATION', 'ProdSettings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'DevSettings')

import configurations
configurations.setup()

app = Celery('runner_recommender_app')

# Using a string here means the worker does not have to serialize the
# configuration object to child process.
# - namespace='CELERY' means all celerey-related configuration keys should
# have a 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# load task modules from all registered Django app configs
app.autodiscover_tasks()

