from tests.conftest import login


def test_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == "Hello, World!"


class TestTopMenu:
    def test_before_login(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"FastAPIr" in response.content
        assert b"Register" in response.content
        assert b"Log In" in response.content
        assert b"Posts" in response.content

    def test_after_login(self, client):
        _ = login(client)

        response = client.get("/")
        assert b"FastAPIr" in response.content
        assert b"Register" not in response.content
        assert b"Log In" not in response.content
        assert b"Log Out" in response.content
        assert b"test_user" in response.content


def test_display_content(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"test title" in response.content
    assert b"by test_user on 2021-04-01" in response.content
    assert b"test\nbody" in response.content


class TestForUsersAlreadyPosted:
    def test_display_new_link(self, client):
        _ = login(client)

        response = client.get("/")

        assert response.status_code == 200
        assert b"New" in response.content

    def test_display_edit_link(self, client):
        _ = login(client)

        response = client.get("/")

        assert response.status_code == 200
        assert b"Edit" in response.content


class TestForUsersNotPosted:
    def test_display_new_link(self, client):
        _ = login(client, username="test_user2")

        response = client.get("/")

        assert response.status_code == 200
        assert b"New" in response.content

    def test_not_display_edit_link(self, client):
        _ = login(client, username="test_user2")

        response = client.get("/")

        assert response.status_code == 200
        assert b"Edit" not in response.content
