from sqlalchemy import create_engine
from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker
from fastapi.requests import Request

database_url = 'postgresql://postgres:pavel@localhost/video_hosting'

engine = create_engine(database_url)

database = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()


def get_db(request: Request):
    return request.state.db
