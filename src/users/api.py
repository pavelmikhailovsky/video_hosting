from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import service, auth, schemas
from core.db import get_db

users_app = APIRouter(prefix='/users', tags=['users'])


@users_app.post('/token')
async def login(db: Session = Depends(get_db), data: OAuth2PasswordRequestForm = Depends()):
    return service.access_token(db, data)


@users_app.get('/me')
async def users_me(db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    return service.get_current_user(db, token)


@users_app.post('/create')
async def create_user(data: schemas.UserInDB, db: Session = Depends(get_db)):
    return service.create_user(data, db)
