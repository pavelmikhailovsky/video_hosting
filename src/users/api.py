import typing as t

from fastapi import APIRouter, Depends
from  fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from . import service, auth, schemas
from core.db import get_db

users_app = APIRouter(prefix='/users', tags=['users'])


@users_app.post('/token')
async def login(db: Session = Depends(get_db), data: schemas.UserTokenLogin = Depends()):
    return service.access_token(db, data)


@users_app.get('/me', response_model=schemas.User)
async def users_me(db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth.oauth2_scheme)):
    return service.get_current_user(db, token)


@users_app.post('/create', response_model=schemas.UserInDB, status_code=201)
async def create_user(data: schemas.UserInDB = Depends(), db: Session = Depends(get_db)):
    return service.create_user(db, data)


@users_app.put('/update')
async def update_user(db: Session = Depends(get_db),
                      data: schemas.UserUpdate = Depends(),
                      token: HTTPAuthorizationCredentials = Depends(auth.oauth2_scheme)):
    return service.UpdateUser(db, data, token).returning_result()


@users_app.get('/{user_id}', response_model=schemas.User)
async def get_user_by_id(user_id: int,
                         db: Session = Depends(get_db),
                         token: HTTPAuthorizationCredentials = Depends(auth.oauth2_scheme)):
    return service.user_by_id(db, user_id, token)
