from celery import Celery
from app.core.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery_app = Celery(
    "task_system",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


import app.tasks.celery_tasks

