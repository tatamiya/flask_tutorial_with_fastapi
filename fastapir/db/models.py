from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

MAX_USERNAME_LENGTH = 32
MAX_HASHED_PASSWORD_LENGTH = 256
MAX_BLOG_TITLE_LENGTH = 64
MAX_BLOG_BODY_LENTGH = 1024


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(MAX_USERNAME_LENGTH), unique=True, index=True)
    hashed_password = Column(String(MAX_HASHED_PASSWORD_LENGTH))


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(MAX_BLOG_TITLE_LENGTH), index=True)
    body = Column(String(MAX_BLOG_BODY_LENTGH))
    created_at = Column(Date)
    author_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", lazy="select")
