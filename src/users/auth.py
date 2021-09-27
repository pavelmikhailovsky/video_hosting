import logging
from datetime import datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.users.models import User

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099d4f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    type_token: str


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = HTTPBearer()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def authentication_user(db: Session, username: str, password: str):
    users = db.query(User).filter(User.username == username).all()  # TODO find other solution
    for user in users:
        return user if verify_password(password, user.password) else None


def decode_token_for_username(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        return username
    except jwt.exceptions.DecodeError:
        raise credentials_exception
