from random import randint

from pydantic import BaseSettings
from fastapi_mail import ConnectionConfig


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1.0'
    PORT: int = 8001
    HOST: str = '127.0.0.1'


settings = Settings()

conf_email = ConnectionConfig(
    MAIL_USERNAME = "fastapi.test.send.email",
    MAIL_PASSWORD = "FastapiTest1",
    MAIL_FROM = "fastapi.test.send.email@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Confirmation email address",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

number_for_confirmation = randint(1, 1000000)

template_email = f'You code for confirmation email address {number_for_confirmation}'
