from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette import status

from . import auth, schemas
from .models import User


def access_token(db: Session, data: OAuth2PasswordRequestForm):
    user = auth.authentication_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    token = auth.create_access_token({'sub': user.username})
    return {'access_token': token, 'type_token': 'bearer'}


def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Cold not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    username = auth.decode_token_for_username(token, credentials_exception)
    if username is None:
        raise credentials_exception

    user = db.query(User).filter(User.username == username)
    if user is None:
        raise credentials_exception

    return user


def create_user(data: schemas.UserInDB, db: Session):
    try:
        hashed_password = auth.get_password_hash(data.password)
        db_user = User(username=data.username, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        return {'detail': f"Username '{data.username}' is was taken"}
