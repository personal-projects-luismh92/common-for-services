from celery import Celery
import os

# Load environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Celery
celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,  # Optional: Store task results
    include=["celery_worker.tasks"]  # 👈 Ensures tasks are registered
)

celery.conf.update(
    task_routes={
        "celery_worker.tasks.send_email_task": {"queue": "email_queue"},
        "celery_worker.tasks.log_to_logging_service_task": {"queue": "logging_queue"},
    },
    result_expires=3600,  # Expire results after 1 hour
)
