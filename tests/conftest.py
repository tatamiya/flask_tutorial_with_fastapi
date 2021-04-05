import os
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapir.main import app
from fastapir.db import crud
from fastapir.db.database import Base, get_db

test_db = tempfile.NamedTemporaryFile(suffix=".db")


engine = create_engine(
    "sqlite:///" + test_db.name, connect_args={"check_same_thread": False}
)

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


test_user = crud.UserCreate(
    username="test_user",
    hashed_password="$2b$12$b0QaOkAp1tGptfKqW0JRBeSu1Vn9HGHusMf7BPSEbDkGxgbz5KXWS",
)
for db in override_get_db():
    crud.create_user(db, test_user)

app.dependency_overrides[get_db] = override_get_db


@app.on_event("shutdown")
def teardown_db():
    Base.metadata.drop_all(bind=engine)
    os.close(test_db)
