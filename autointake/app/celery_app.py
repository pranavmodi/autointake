import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Construct the database URL for Celery
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "autointake")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# It's good practice to have a separate DB for celery, but for now this is fine.
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", DATABASE_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", DATABASE_URL)

celery_app = Celery(
    "autointake",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["autointake.app.tasks.intake_tasks"]
)

# Optional configuration
celery_app.conf.update(
    task_track_started=True,
    timezone=os.getenv("TIMEZONE", "UTC"),
)

# Celery Beat Schedules
celery_app.conf.beat_schedule = {
    'check-for-reminders-and-escalations': {
        'task': 'autointake.app.tasks.intake_tasks.check_for_reminders_and_escalations',
        # Runs every 5 minutes
        'schedule': crontab(minute='*/5'),
    },
} 