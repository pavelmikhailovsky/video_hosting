from fastapi.testclient import TestClient

from main import app
from core.config import Settings
from core.db import get_db
from core.tests.test_db import override_get_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

url = f'{Settings.API_V1_STR}/users'


def test_create_user():
    response = client.post(f'{url}/create', params={'username': 'testuser', 'password': 'testpassword'})
    print(f'{response.url}')
    data = response.json()
    assert response.status_code == 201
    assert data['username'] == 'testuser'

