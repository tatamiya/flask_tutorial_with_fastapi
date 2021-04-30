import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapir.config import Settings

SQLALCHEMY_DATABASE_URL = Settings().database_url

if os.getenv("GAE_APPLICATION", None):
    connect_args = {}
else:
    connect_args = {"check_same_thread": False}

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
