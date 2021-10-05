import pytest

from core.config import settings
from core.db import get_db
from core.tests.test_db import override_get_db
from main import app

app.dependency_overrides[get_db] = override_get_db

url = f'http://127.0.0.1:8001/{settings.API_V1_STR}/video'

# TODO write tests later
