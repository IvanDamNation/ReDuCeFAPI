from celery import Celery

from src.config import CeleryConfig


app = Celery("ddup_worker")

app.conf.update(
    broker_url=CeleryConfig.CELERY_BROKER,
    result_backend=CeleryConfig.CELERY_BACKEND,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=10,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    task_reject_on_worker_lost=True,
    task_acks_late=True,
    include=['src.worker.tasks'],
    broker_transport_options = {
    'visibility_timeout': 3600, 
    'health_check_interval': 10,
    'socket_keepalive': True
    },
)