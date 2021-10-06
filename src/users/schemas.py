import typing as t
from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str
    create_at: datetime
    is_active: bool
    is_staff: bool

    class Config:
        orm_mode = True


class UserInDB(BaseModel):
    username: str
    password: str
    email: t.Optional[EmailStr] = None

    class Config:
        orm_mode = True


class UserTokenLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    new_username: t.Optional[str]
    current_password: t.Optional[str]
    new_password: t.Optional[str]
    email: t.Optional[EmailStr]
