import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "outfitcore.settings")

app = Celery("outfitcore")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Agregar la configuración correctamente
app.conf.broker_connection_retry_on_startup = True  

app.autodiscover_tasks()
