import datetime

from sqlalchemy.orm import Session, lazyload
from pydantic import BaseModel

from . import models


class UserCreate(BaseModel):
    username: str
    hashed_password: str


class PostCreate(BaseModel):
    title: str
    body: str
    created_at: datetime.datetime
    author_id: int


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    db_user = models.User(
        username=user.username,
        hashed_password=user.hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_post(db: Session, post: PostCreate):
    db_post = models.Post(
        title=post.title,
        body=post.body,
        created_at=post.created_at,
        author_id=post.author_id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Post)
        .options(lazyload(models.Post.user))
        .order_by(models.Post.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
