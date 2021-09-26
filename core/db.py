from sqlalchemy import create_engine
from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

engine = create_engine('postgresql://postgres:pavel@localhost/video_hosting')

database = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()


def get_db(request: Request):
    return request.state.db
