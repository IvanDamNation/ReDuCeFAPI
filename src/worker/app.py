from kombu import Queue
from celery import Celery

from src.config import CeleryConfig


app = Celery("ddup_worker")

app.conf.update(
    broker_url=CeleryConfig.CELERY_BROKER,
    result_backend=CeleryConfig.CELERY_BACKEND,
    broker_connection_retry_on_startup=True,
    task_queues=[
        Queue("ddup_queue", routing_key="ddup.#"),
    ],
    task_default_queue="ddup_queue",
    worker_send_task_events=True,
    task_send_sent_event=True,
    event_queue_expires=60,
    worker_pool="solo",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    include=["src.worker.tasks"],
    broker_transport_options={
        "visibility_timeout": 3600,
        "health_check_interval": 10,
        "socket_keepalive": True,
    },
)
