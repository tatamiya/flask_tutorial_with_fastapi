from tests.conftest import login


class TestCreatePost:
    def test_display_page(self, client):
        _ = login(client)
        response = client.get("/blog/create")

        assert response.status_code == 200
        assert b"New Post" in response.content
        assert b"Title" in response.content
        assert b"Body" in response.content

    def test_redirect_if_not_logged_in(self, client):

        response = client.get("/blog/create", allow_redirects=False)
        assert response.status_code != 200

    def test_create_post(self, client):
        _ = login(client)

        response = client.post(
            "/blog/create",
            data={"title": "new post", "body": "newly created for test"},
            allow_redirects=True,
        )
        assert response.status_code == 200

        assert b"new post" in response.content
        assert b"newly created for test" in response.content

    def test_create_without_authentication(self, client):
        response = client.post(
            "/blog/create",
            data={"title": "invalid post", "body": "should not be created"},
            allow_redirects=True,
        )
        assert response.status_code == 401


class TestDisplayEditPage:
    def test_display_page(self, client):
        _ = login(client)
        response = client.get("/blog/2/update")

        assert response.status_code == 200
        assert b'Edit "new post"' in response.content

    def test_invalid_access(self, client):
        _ = login(client, username="test_user2")
        response = client.get("/blog/2/update")
        assert response.status_code == 401


class TestUpdatePost:
    def test_update_post(self, client):
        _ = login(client)

        response = client.post(
            "/blog/2/update",
            data={"title": "update post", "body": "update successfully"},
            allow_redirects=True,
        )
        assert response.status_code == 200

        assert b"new post" not in response.content
        assert b"newly created for test" not in response.content

        assert b"update post" in response.content
        assert b"updated successfully" not in response.content

    def test_update_without_authentication(self, client):
        response = client.post(
            "/blog/2/update",
            data={"title": "invalid update", "body": "should not be updated"},
            allow_redirects=True,
        )
        assert response.status_code == 401

    def test_invalid_update(self, client):
        _ = login(client, username="test_user2")

        response = client.post(
            "/blog/2/update",
            data={"title": "invalid update", "body": "should not be updated"},
            allow_redirects=True,
        )
        assert response.status_code == 401

    def test_update_not_found(self, client):
        _ = login(client)
        response = client.post(
            "/blog/99/update",
            data={"title": "does not exist", "body": "cannot be updated"},
            allow_redirects=True,
        )
        assert response.status_code == 404


class TestDeletePost:
    def test_delete_post(self, client):
        _ = login(client)

        response = client.post(
            "/blog/2/delete",
            allow_redirects=True,
        )
        assert response.status_code == 200

        assert b"update post" not in response.content
        assert b"update successfully" not in response.content

    def test_delete_without_authentication(self, client):
        response = client.post(
            "/blog/1/delete",
            allow_redirects=True,
        )
        assert response.status_code == 401

    def test_invalid_delete(self, client):
        _ = login(client, username="test_user2")
        response = client.post(
            "/blog/1/delete",
            allow_redirects=True,
        )
        assert response.status_code == 401

    def test_delete_not_found(self, client):
        _ = login(client)
        response = client.post(
            "/blog/99/delete",
            allow_redirects=True,
        )
        assert response.status_code == 404
