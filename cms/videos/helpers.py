import os

import boto3
from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session

from cms.videos import crud
from cms.videos import models
from cms.videos import tasks
from conf.settings import Settings


def get_file_extension(file_name: str) -> str:
    """
    Returns the file extension of the given file name.
    """
    return os.path.splitext(file_name)[1]


def upload_file_to_s3(
    db: Session, file: UploadFile, object_name: str, video: models.Video
):
    """
    Upload a file to an S3 bucket

    :param db: DB Session
    :param file: File to upload
    :param object_name: New file name for the uploaded file
    :param video: Video object for which the video is related
    :return: video if success else None
    """

    s3_client = boto3.client("s3")
    bucket_name = Settings.BUCKET_NAME

    try:
        s3_client.upload_fileobj(file.file, bucket_name, object_name)
        video = crud.update_file_in_video(db, object_name, video)
        tasks.process_file.delay(video.id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    return video
