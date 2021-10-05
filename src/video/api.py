import typing as t

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.db import get_db
from . import schemas, service
from ..users import auth

video_app = APIRouter(prefix='/video', tags=['video'])


@video_app.post('/upload_description', status_code=201, response_model=schemas.Video)
async def video_description(description: schemas.UploadVideo = Depends(),
                            db: Session = Depends(get_db),
                            token: HTTPAuthorizationCredentials = Depends(auth.oauth2_scheme),
                            ):
    return service.video_description_service(db, description, token)


@video_app.post('/upload', status_code=201)
async def upload_video(video: UploadFile = File(...),
                       db: Session = Depends(get_db),
                       token: HTTPAuthorizationCredentials = Depends(auth.oauth2_scheme),
                       ):
    return service.recording_video(db, video, token)


@video_app.get('/stream_video/{video_id}')
def stream_video(video_id: int, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth.oauth2_scheme)):
    return StreamingResponse(service.iterable_video(db, token, video_id), media_type='video/mp4')


@video_app.get('', response_model=t.List[schemas.Video])
async def get_list_video(db: Session = Depends(get_db),
                         token: HTTPAuthorizationCredentials = Depends(auth.oauth2_scheme)):
    return service.get_list_video_service(db, token)
