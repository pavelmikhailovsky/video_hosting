import os
import shutil
import aiofiles
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from src.users.service import get_current_user
from .models import Video
from .schemas import UploadVideo
from ..users.models import User


def get_list_video_service(db: Session, token: HTTPAuthorizationCredentials):
    _ = get_current_user(db, token)
    video = db.query(Video).all()
    return video


def video_description_service(db: Session, video_description: UploadVideo, token: HTTPAuthorizationCredentials):
    user = get_current_user(db, token)
    db_video = Video(**video_description.dict())
    db_video.address = user.video_path
    user.video_path = ''
    db_video.user_id = user.id
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def recording_video(db: Session, video: UploadFile, token: HTTPAuthorizationCredentials):
    user = get_current_user(db, token)
    if video.content_type == 'video/mp4':
        path = f'{os.getcwd()}/media/video/{user.id}/'
        if not os.path.exists(path):
            os.makedirs(path)
        path = f'{path}{uuid4()}.mp4'
        with open(f'{path}', 'wb') as f:
            shutil.copyfileobj(video.file, f)
        writing_video_path(db, user, path)
        return path


def writing_video_path(db: Session, user: User, path: str):
    try:
        if not user.video_path:
            user.video_path = path
        else:
            raise Exception
    except Exception:
        os.remove(user.video_path)  # TODO fix problem
        user.video_path = ''
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail='Resetting uploading user video')
    finally:
        db.commit()


def iterable_video(db: Session, token: HTTPAuthorizationCredentials, video_id: int):
    _ = get_current_user(db, token)
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Video is not finded')
    with open(video.address, 'rb') as video:
        yield from video
