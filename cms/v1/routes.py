from uuid import uuid4

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from cms.v1 import schemas
from cms.videos import crud
from cms.videos.helpers import get_file_extension
from cms.videos.helpers import upload_file_to_s3
from conf.db.dependencies import get_db

router = APIRouter()


def get_video_or_raise_exception(db: Session, video_id: int):
    db_video = crud.get_video(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video


@router.get("/videos/", response_model=list[schemas.Video])
async def list_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    videos = crud.get_videos(db, skip, limit)
    return videos


@router.post("/videos/", response_model=schemas.Video)
async def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    db_video = crud.create_video(db, video=video)
    return db_video


@router.get("/videos/{video_id}/", response_model=schemas.Video)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    db_video = get_video_or_raise_exception(db, video_id)
    return db_video


@router.patch("/videos/{video_id}/", response_model=schemas.Video)
async def update_video(
    video_id: int, video: schemas.VideoUpdate, db: Session = Depends(get_db)
):
    db_video = get_video_or_raise_exception(db, video_id)

    updated_video = crud.update_video(db, db_video, video)
    return updated_video


@router.post("/videos/{video_id}/upload/", response_model=schemas.Video)
async def upload_video(
    video_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    video = get_video_or_raise_exception(db, video_id)
    file_extension = get_file_extension(file.filename)
    object_name = f"{uuid4()}{file_extension}"
    video = upload_file_to_s3(db, file, object_name, video)
    return video


@router.delete("/videos/{video_id}/")
async def delete_video(video_id: int, db: Session = Depends(get_db)):
    db_video = get_video_or_raise_exception(db, video_id)
    crud.delete_video(db, db_video)
    return JSONResponse({}, status_code=204)
