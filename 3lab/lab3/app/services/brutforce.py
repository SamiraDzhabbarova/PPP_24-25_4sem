from app.celery.tasks import run_brutforce_task

def start_brutforce(hash_value: str, charset: str, max_length: int, user_id: int) -> str:
    task = run_brutforce_task.delay(user_id, hash_value, charset, max_length)
    return task.id

def get_task_status(task_id: str) -> dict:
    async_result = run_brutforce_task.AsyncResult(task_id)
    return {
        "status": async_result.status,
        "progress": 0 if not async_result.ready() else 100,
        "result": async_result.result if async_result.ready() else None
    }


