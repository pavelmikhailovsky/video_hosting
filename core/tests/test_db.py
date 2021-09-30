from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from starlette.requests import Request
from starlette.responses import Response

from core.db import Base


engine = create_engine('postgresql://postgres:pavel@localhost/test_video_hosting')

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)


def override_get_db(request: Request):
    request.state.db = TestSession()
    return request.state.db
