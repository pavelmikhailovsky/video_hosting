import typing as t
from datetime import datetime

from pydantic import BaseModel, EmailStr, validator, ValidationError


class BaseUserUpdateOrDB(BaseModel):
    email: t.Optional[EmailStr]
    phone_number: t.Optional[str]

    @validator('phone_number')
    def phone_number(cls, value):
        if not value[0] == '+':
            raise ValidationError('Phone number is not correct')
        return value


class User(BaseModel):
    id: int
    username: str
    create_at: datetime
    is_active: bool
    is_staff: bool

    class Config:
        orm_mode = True


class UserInDB(BaseUserUpdateOrDB):
    username: str
    password: str

    class Config:
        orm_mode = True


class UserTokenLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseUserUpdateOrDB):
    new_username: t.Optional[str]
    current_password: t.Optional[str]
    new_password: t.Optional[str]
