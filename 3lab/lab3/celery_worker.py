from app.celery.app import celery_app
import app.celery.tasks
if __name__ == "__main__":
    celery_app.worker_main()
