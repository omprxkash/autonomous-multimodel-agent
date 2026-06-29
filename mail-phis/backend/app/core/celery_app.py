from celery import Celery
from .config import settings

celery = Celery(
    "mailrecon",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.workers.tasks"],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    task_routes={
        "app.workers.tasks.run_email_pipeline": {"queue": "email"},
        "app.workers.tasks.run_url_pipeline": {"queue": "url"},
    },
)
