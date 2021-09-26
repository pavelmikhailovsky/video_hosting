import typing as t

from pydantic import BaseModel


class VideoBase(BaseModel):
    description: str

    class Config:
        orm_mode = True


class Video(BaseModel):
    id: int
    address: str
    description: str

    class Config:
        orm_mode = True


class UploadVideo(VideoBase):
    pass
