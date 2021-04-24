from fastapir.db import crud
from .conftest import override_get_db


class TestLogin:
    def test_login_page(self, client):
        assert client.get("/auth/login").status_code == 200

    def test_valid_access(self, client):

        response = client.post(
            "/auth/login",
            data={"username": "test_user", "password": "test_password"},
            allow_redirects=True,
        )
        assert response.status_code == 200

    def test_invalid_access(self, client):
        response = client.post(
            "/auth/login",
            data={"username": "test_user", "password": "invalid_password"},
            allow_redirects=True,
        )
        assert response.status_code == 400


def test_logout(client):

    response = client.get("/auth/logout", cookies={"username": "test_user"})
    assert response.status_code == 200


class TestRegister:
    def test_register_page(self, client):
        assert client.get("/auth/register").status_code == 200

    def test_register_user(self, client):

        response = client.post(
            "/auth/register",
            data={"username": "a", "password": "a"},
            allow_redirects=True,
        )
        assert response.status_code == 200

        for db in override_get_db():
            user = crud.get_user_by_name(db, "a")
        assert user is not None

    def test_already_registered(self, client):

        response = client.post(
            "/auth/register",
            data={"username": "test_user", "password": "test"},
            allow_redirects=True,
        )
        assert response.status_code == 400
