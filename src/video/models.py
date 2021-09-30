from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from core.db import Base


class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    time_uploading = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String(1000))

    uploader = relationship('User')
