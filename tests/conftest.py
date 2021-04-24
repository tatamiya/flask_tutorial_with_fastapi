import datetime
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapir.db import crud
from fastapir.db.database import Base, get_db
from fastapir.main import app

test_db = tempfile.NamedTemporaryFile(suffix=".db")

# TestingSessionLocal = create_db_session()

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
test_user2 = crud.UserCreate(
    username="test_user2",
    hashed_password="$2b$12$b0QaOkAp1tGptfKqW0JRBeSu1Vn9HGHusMf7BPSEbDkGxgbz5KXWS",
)

test_post = crud.PostCreate(
    title="test title",
    body="test\nbody",
    created_at=datetime.datetime(2021, 4, 1, 0, 0, 0),
    author_id=1,
)

for db in override_get_db():
    crud.create_user(db, test_user)
    crud.create_user(db, test_user2)
    crud.create_post(db, test_post)

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)


def login(client, username="test_user", password="test_password"):

    response = client.post(
        "/auth/login",
        data={"username": username, "password": password},
        allow_redirects=True,
    )
    return response
