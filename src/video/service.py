import os
import shutil
import aiofiles
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from .models import Video
from .schemas import UploadVideo


def get_list_video_service(db: Session):
    return db.query(Video).all()


def video_description_service(db: Session, video_description: UploadVideo, video: UploadFile):
    db_video = Video(**video_description.dict())
    db_video.address = recording_video(video)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def recording_video(video: UploadFile):
    if video.content_type == 'video/mp4':
        path = f'{os.getcwd()}/media/video/1/'
        if not os.path.exists(path):
            os.makedirs(path)
        path = f'{path}{uuid4()}.mp4'
        with open(f'{path}', 'wb') as f:
            shutil.copyfileobj(video.file, f)
        return path


string = "E:\\dev\\python\\video_hosting_back/media/video/1/28b550ec-c656-45c8-a6e8-07c25b312437.mp4"


def iterable_video():
    with open(string, 'rb') as video:
        yield from video
