from fastapi.testclient import TestClient

from fastapir.main import app
from fastapir.auth import get_user_by_name, get_db

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

        db = get_db()
        user = get_user_by_name(db, "a")
        assert user is not None

    def test_already_registered(self):

        response = client.post(
            "/auth/register",
            data={"username": "test_user", "password": "test"},
            allow_redirects=True,
        )
        assert response.status_code == 400
