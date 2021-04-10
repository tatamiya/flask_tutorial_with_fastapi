from fastapi.testclient import TestClient

from fastapir.main import app
from fastapir.db import crud
from .conftest import override_get_db


client = TestClient(app)


def test_display_content():
    response = client.get("/")
    assert response.status_code == 200
    assert b"test title" in response.content
    assert b"by test_user on 2021-04-01" in response.content
    assert b"test\nbody" in response.content
