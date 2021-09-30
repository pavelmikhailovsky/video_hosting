import logging
import inspect
import typing as t

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette import status

from . import auth, schemas
from .models import User


def access_token(db: Session, data: schemas.UserTokenLogin):
    user = auth.authentication_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    token = auth.create_access_token({'sub': user.username})
    return {'access_token': token, 'type_token': 'Bearer'}


def get_current_user(db: Session, token: HTTPAuthorizationCredentials):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Cold not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    logging.debug(f'this is func {inspect.currentframe().f_code.co_name}')

    username = auth.decode_token_for_username(token.credentials, credentials_exception)
    if username is None:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()  # TODO find other solution
    if not user:
        raise credentials_exception

    return user


def create_user(db: Session, data: schemas.UserInDB):
    try:
        hashed_password = auth.get_password_hash(data.password)
        db_user = User(username=data.username, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        return {'detail': f"Username '{data.username}' is was taken"}


def user_by_id(db: Session, user_id: int, token: HTTPAuthorizationCredentials):
    _ = get_current_user(db, token)
    return db.query(User).filter(User.id == user_id).first()  # TODO find other solution


class UpdateUser:
    def __init__(self, db: Session, data: schemas.UserUpdate, token: HTTPAuthorizationCredentials):
        self.db = db
        self.data = data
        self.token = token

    def returning_result(self):
        result = {}
        user = get_current_user(self.db, self.token)
        if self.data.new_username:
            result.update(self.new_username(user))

        if self.data.new_password:
            if not self.data.current_password and auth.verify_password(self.data.current_password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Password is not entered or incorrect'
                )
            result.update(self.new_password(user))

        return result

    def new_username(self, user):
        unique_username = self.db.query(User).filter(User.username == self.data.new_username).first()  # TODO find other solution
        if unique_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Username {self.data.new_username} already exist'
            )
        user.username = self.data.new_username
        self.db.commit()
        return {'username': self.data.new_username}

    def new_password(self, user):
        hashed_password = auth.get_password_hash(self.data.new_password)
        user.password = hashed_password
        self.db.commit()
        return {'password': 'is changed'}








