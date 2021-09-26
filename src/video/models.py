from sqlalchemy import Column, Integer, String, ForeignKey

from core.db import Base


class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    description = Column(String(1000))
