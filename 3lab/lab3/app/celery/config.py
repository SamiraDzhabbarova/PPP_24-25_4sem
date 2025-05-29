from celery import Celery
from app.celery import tasks

app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

app.conf.task_track_started = True
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
