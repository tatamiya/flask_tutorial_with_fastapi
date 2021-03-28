from fastapi.testclient import TestClient

from fastapir.main import app

client = TestClient(app)


def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == "Hello, World!"


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert b"FastAPIr" in response.content
    assert b"Register" in response.content
    assert b"Log In" in response.content
    assert b"Posts" in response.content


def test_index_after_login():
    response = client.get("/", cookies={"username": "test_user"})
    assert b"Register" not in response.content
    assert b"Log In" not in response.content
    assert b"Log Out" in response.content
    assert b"test_user" in response.content
