from sqlalchemy import Integer, String, DateTime, Column, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.db import Base
from src.video.models import Video


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(200), unique=True, index=True)
    password = Column(String)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    is_staff = Column(Boolean, server_default='f')
    is_active = Column(Boolean, server_default='t')
    video_path = Column(String, server_default='')

    video = relationship("Video", backref='user')
