import typing as t
from datetime import datetime

from pydantic import BaseModel

from src.video.schemas import Video


class User(BaseModel):
    id: int
    username: str
    create_at: datetime
    video: t.List[Video] = []
    is_active: bool
    is_staff: bool

    class Config:
        orm_mode = True


class UserInDB(BaseModel):
    username: str
    password: str


class UserTokenLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    new_username: t.Optional[str]
    current_password: t.Optional[str]
    new_password: t.Optional[str]
