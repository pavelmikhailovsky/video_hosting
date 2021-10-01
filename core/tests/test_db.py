from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.requests import Request

from core.db import Base

url_database = 'postgresql://postgres:pavel@localhost/test_video_hosting'

if database_exists(url_database):
    drop_database(url_database)

create_database(url_database)

engine = create_engine(url_database)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# импорты обязательны только после инициализации Base
from src.users.models import User
from src.video.models import Video

Base.metadata.create_all(bind=engine)


def override_get_db(request: Request):
    request.state.db = TestSession()
    return request.state.db
