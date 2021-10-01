from fastapi import params
import pytest
from httpx import AsyncClient

from main import app
from core.config import settings
from core.db import get_db
from core.tests import test_db

app.dependency_overrides[get_db] = test_db.override_get_db

url = f'http://127.0.0.1:8001{settings.API_V1_STR}/users'

class Token:
    _token = 'something token'

    def __init__(self, token) -> None:
        self._token = token

    @classmethod
    def get_token(cls):
        return cls._token


token = ''


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url=url) as async_client:
        response = await async_client.post(
            '/create', params={'username': 'testuser', 'password': 'testpassword'}
        )
    data = response.json()
    assert response.status_code == 201
    assert data['username'] == 'testuser'


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url=url) as async_client:
        correct_response = await async_client.post(
            '/token', params={'username': 'testuser', 'password': 'testpassword'}
        )
        incorrect_response = await async_client.post(
            '/token', params={'username': 'testuser123', 'password': 'testpassword'}
        )
    assert correct_response.status_code == 200
    assert incorrect_response.status_code == 401
    data = correct_response.json()
    token = Token(f'{data["type_token"]} {data["access_token"]}')
    incorrect_data = incorrect_response.json()
    assert incorrect_data['detail'] == 'Incorrect username or password'


@pytest.mark.asyncio
async def test_user_info_about_me():
    async with AsyncClient(app=app, base_url=url) as async_client:
        correct_response = await async_client.get(
            '/me', headers={'Authorization': Token.get_token()}
        )
        print(Token.get_token())
        incorrect_response = await async_client.get(
            '/me', headers={'Authorization': f'{Token.get_token()}abc'}
        )
    assert correct_response.status_code == 200
    assert incorrect_response.status_code == 422
    data = correct_response.json()
    assert data['username'] == 'testuser'
