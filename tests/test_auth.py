from fastapir.db import crud

from .conftest import login, override_get_db


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
        assert b"Authentication failed" in response.content


def test_logout(client):
    _ = login(client)
    resp_before_logout = client.get("/")
    assert b"Log Out" in resp_before_logout.content

    resp_after_logout = client.get("/auth/logout")
    assert b"Log Out" not in resp_after_logout.content


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
        assert b"Already registered" in response.content
