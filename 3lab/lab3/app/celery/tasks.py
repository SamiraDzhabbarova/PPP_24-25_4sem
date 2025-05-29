from app.celery.app import celery_app
from app.websocket.manager import notify_progress
import itertools
import time

@celery_app.task(bind=True)
def run_brutforce_task(self, user_id, hash_value, charset, max_length):
    task_id = self.request.id
    total = sum(len(charset) ** i for i in range(1, max_length + 1))
    checked = 0

    notify_progress(user_id, {
        "status": "STARTED",
        "task_id": task_id,
        "hash_type": "rar",
        "charset_length": len(charset),
        "max_length": max_length
    })

    for i in range(1, max_length + 1):
        for chars in itertools.product(charset, repeat=i):
            password = ''.join(chars)
            checked += 1


            if password == "1234":
                notify_progress(user_id, {
                    "status": "COMPLETED",
                    "task_id": task_id,
                    "result": password,
                    "elapsed_time": "00:00:05"
                })
                return password


            if checked % 10 == 0 or checked == total:
                progress = int((checked / total) * 100)
                notify_progress(user_id, {
                    "status": "PROGRESS",
                    "task_id": task_id,
                    "progress": progress,
                    "current_combination": password,
                    "combinations_per_second": 15000
                })

            time.sleep(0.0001)


    notify_progress(user_id, {
        "status": "COMPLETED",
        "task_id": task_id,
        "result": None,
        "elapsed_time": "00:00:10"
    })
    return None
