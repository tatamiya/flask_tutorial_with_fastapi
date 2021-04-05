from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapir.main import app
from fastapir.db import crud
from fastapir.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
if Base.metadata.tables:
    Base.metadata.drop_all(bind=engine)

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


client = TestClient(app)


def test_login_page():
    assert client.get("/auth/login").status_code == 200


class TestLogin:
    def test_valid_access(self):

        response = client.post(
            "/auth/login",
            data={"username": "test_user", "password": "test_password"},
            allow_redirects=True,
        )
        assert response.status_code == 200

    def test_invalid_access(self):
        response = client.post(
            "/auth/login",
            data={"username": "test_user", "password": "invalid_password"},
            allow_redirects=True,
        )
        assert response.status_code == 400


def test_logout():

    response = client.get("/auth/logout", cookies={"username": "test_user"})
    assert response.status_code == 200


class TestRegister:
    def test_register_page(self):
        assert client.get("/auth/register").status_code == 200

    def test_register_user(self):

        response = client.post(
            "/auth/register",
            data={"username": "a", "password": "a"},
            allow_redirects=True,
        )
        assert response.status_code == 200

        for db in override_get_db():
            user = crud.get_user_by_name(db, "a")
        assert user is not None

    def test_already_registered(self):

        response = client.post(
            "/auth/register",
            data={"username": "test_user", "password": "test"},
            allow_redirects=True,
        )
        assert response.status_code == 400
