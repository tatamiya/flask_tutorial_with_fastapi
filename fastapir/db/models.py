from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(256))


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), index=True)
    body = Column(String(1024))
    created_at = Column(Date)
    author_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", lazy="select")
