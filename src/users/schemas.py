import typing as t
from datetime import datetime

from pydantic import BaseModel

from src.video.schemas import Video


class User(BaseModel):
    id: int
    username: str
    create_at: datetime
    video: Video
    is_active: bool
    is_staff: bool


class UserInDB(BaseModel):
    username: str
    password: str
