from celery import Celery

from conf.settings import Settings

CELERY_BROKER_URL = (
    f"amqp://{Settings.RABBITMQ_USER}:{Settings.RABBITMQ_PASSWORD}@"
    f"{Settings.RABBITMQ_HOST}:{Settings.RABBITMQ_PORT}/{Settings.RABBITMQ_VHOST}"
)

CELERY_BACKEND_URL = (
    f"redis://{Settings.REDIS_HOST}:{Settings.REDIS_PORT}/{Settings.REDIS_DB}"
)


celery_app = Celery(
    "fastapi-template", broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL
)
celery_app.autodiscover_tasks(["cms.videos.tasks"], force=True)
