from sqlalchemy.orm import Session
from pydantic import BaseModel

from . import models


class User(BaseModel):
    user_id: int
    username: str
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    hashed_password: str


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
