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


def test_display_new_link():
    response = client.get("/", cookies={"user_id": "1"})

    assert response.status_code == 200
    assert b"New" in response.content


class TestCreateBlog:
    def test_display_page(self):
        response = client.get("/blog/create", cookies={"user_id": "1"})

        assert response.status_code == 200
        assert b"New Post" in response.content
        assert b"Title" in response.content
        assert b"Body" in response.content

    def test_redirect_if_not_logged_in(self):
        response = client.get(
            "/blog/create", cookies={"user_id": None}, allow_redirects=False
        )
        assert response.status_code != 200
