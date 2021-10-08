import logging
import inspect
import typing as t

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette import status

from . import auth, schemas
from .models import User
from core.config import (template_email, conf_email, number_for_confirmation_email,
                        client, phone, number_for_confirmation_phone,)

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
        return {'username': data.username, 'password': data.password}
    except IntegrityError:
        return {'detail': f"Username '{data.username}' is was taken"}


def user_by_id(db: Session, user_id: int, token: HTTPAuthorizationCredentials):
    _ = get_current_user(db, token)
    return db.query(User).filter(User.id == user_id).first()


async def email_confirmation(db: Session, token: HTTPAuthorizationCredentials):
    user = get_current_user(db, token)
    if user.email:
        message = MessageSchema(
            subject='Video hosting',
            recipients=[user.email,],
            body=template_email,
            subtype='plain'
        )
        fm = FastMail(conf_email)
        await fm.send_message(message)
        return {'email': 'Message send'}
    raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f'User does not have email'
            )


def phone_confirmation(db: Session, token: HTTPAuthorizationCredentials):
    user = get_current_user(db, token)
    if not user.phone_number:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f'User does not have phone number'
            )
    message = client.messages.create(
        body=f'You code for confirmation phone number {number_for_confirmation_phone}',
        from_=phone,
        to=user.phone_number,
    )
    return {'message': message.body}


class ExaminationNumber:
    _exception = HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Number for confirmation is not valid'
                    )

    def __init__(self, action, db, token, number_confirmation):
        self.action = action
        self.db = db
        self.token = token
        self.number_confirmation = number_confirmation
        self.user = get_current_user(self.db, self.token)

    def action(self):
        result = {}
        if self.action == 'email':
            result.update(self._examination_number_email())
        elif self.action == 'phone':
            result.update(self._examination_phone_number())
        return result

    def _examination_number_email(self):
        if not self.user.email_confirmation:
            if self.number_confirmation == number_for_confirmation_email:
                self.user.email_confirmation = True
                self.db.commit()
                return {'status': 'Email address is confirmation'}
            raise self._exception
        if self.number_confirnumber_confirmationamtion == number_for_confirmation_email:
            self.user.email_confirmation = False
            self.db.commit()
            return {'status': 'Email addres now is not confirmationed'}
        raise self._exception

    def _examination_number_phone(self):
        if not self.user.phone_number_confirmation:
            if self.number_confirmation == number_for_confirmation_phone:
                self.user.phone_number_confirmation = True
                self.db.commit()
                return {'status': 'Phone number is confirmation'}
            raise self._exception
        if self.number_confirmation == number_for_confirmation_phone:
            self.user.phone_number_confirmation = False
            self.db.commit()
            return {'status': 'Phone number now is not confirmationed'}
        raise self._exception

class UpdateUser:
    def __init__(self, db: Session, data: schemas.UserUpdate, token: HTTPAuthorizationCredentials):
        self.db = db
        self.data = data
        self.token = token

    async def returning_result(self):
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

        if self.data.email:
            result_change = await self.change_email(user)
            result.update(result_change)

        return result

    def new_username(self, user):
        unique_username = self.db.query(User).filter(User.username == self.data.new_username).first()
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

    async def change_email(self, user):
        if not user.email_confirmation:
            user.email = self.data.email
            self.db.commit()
            return await email_confirmation(self.db, self.token)
        return await email_confirmation(self.db, self.token)








