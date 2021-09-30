import typing as t

from pydantic import BaseModel

from src.users.schemas import User


class VideoBase(BaseModel):
    description: str

    class Config:
        orm_mode = True


class Video(BaseModel):
    id: int
    address: str
    description: str
    uploader: User

    class Config:
        orm_mode = True


class UploadVideo(VideoBase):
    pass
