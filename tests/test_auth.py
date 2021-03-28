from fastapi.testclient import TestClient

from fastapir.main import app

client = TestClient(app)


def test_login_page():
    assert client.get("/auth/login").status_code == 200


def test_login():

    response = client.post(
        "/auth/login", data={"username": "test_user"}, allow_redirects=True
    )
    assert response.status_code == 200


def test_logout():

    response = client.get("/auth/logout", cookies={"username": "test_user"})
    assert response.status_code == 200
