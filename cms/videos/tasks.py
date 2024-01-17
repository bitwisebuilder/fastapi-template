from time import sleep

from sqlalchemy.orm import Session

from cms.videos import crud
from cms.videos.models import StatusChoice
from conf._celery.app import celery_app
from conf.db.dependencies import with_db_session


@celery_app.task(bind=True, name="process.file")
@with_db_session
def process_file(self, video_id: int, db: Session):
    video = crud.get_video(db, video_id)
    crud.update_status_in_video(db, StatusChoice.PROCESSING, video)
    try:
        print(f"Going in Sleep for {video_id}")
        sleep(30)
        print(f"Came out of Sleep for {video_id}")
        crud.update_status_in_video(db, StatusChoice.PROCESSED, video)
    except Exception as err:
        print(f"Processing failed for video[{video_id}] because of {err}")
        crud.update_status_in_video(db, StatusChoice.FAILED, video)
