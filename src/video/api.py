import typing as t

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette.requests import Request

from core.db import get_db
from . import schemas, service

video_app = APIRouter(prefix='/video', tags=['video'])


# @video_app.post('/upload_description', status_code=201)
# async def video_description(description: schemas.UploadVideo,
#                             video: UploadFile = File(...),
#                             db: Session = Depends(get_db),
#                             ):
#     return service.video_description_service(db, description, video)


@video_app.post('/upload', status_code=201)
async def upload_video(video: UploadFile = File(...),
                       db: Session = Depends(get_db),
                       ):
    return service.recording_video(video)


@video_app.get('/stream_video')
def stream_video(db: Session = Depends(get_db)):
    return StreamingResponse(service.iterable_video(), media_type='video/mp4')


@video_app.get('', response_model=t.List[schemas.Video])
async def get_list_video(db: Session = Depends(get_db)):
    return service.get_list_video_service(db)
