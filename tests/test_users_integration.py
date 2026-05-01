import pytest


class TestUserRegister:

    def test_register_success(self, client):
        res = client.post("/users/register", json={
            "username": "niharika",
            "email": "niharika@example.com",
            "password": "secret123"
        })
        assert res.status_code == 201
        data = res.json()
        assert data["username"] == "niharika"
        assert data["email"] == "niharika@example.com"
        assert "id" in data
        assert "password" not in data
        assert "password_hash" not in data

    def test_register_duplicate_username(self, client):
        client.post("/users/register", json={
            "username": "dupuser",
            "email": "first@example.com",
            "password": "pass123"
        })
        res = client.post("/users/register", json={
            "username": "dupuser",
            "email": "second@example.com",
            "password": "pass123"
        })
        assert res.status_code == 400
        assert "already taken" in res.json()["error"]

    def test_register_duplicate_email(self, client):
        client.post("/users/register", json={
            "username": "user1",
            "email": "shared@example.com",
            "password": "pass123"
        })
        res = client.post("/users/register", json={
            "username": "user2",
            "email": "shared@example.com",
            "password": "pass123"
        })
        assert res.status_code == 400
        assert "already registered" in res.json()["error"]

    def test_register_invalid_email(self, client):
        res = client.post("/users/register", json={
            "username": "baduser",
            "email": "not-an-email",
            "password": "pass123"
        })
        assert res.status_code == 400


class TestUserLogin:

    def test_login_success(self, client):
        client.post("/users/register", json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "mypassword"
        })
        res = client.post("/users/login", params={
            "username": "loginuser",
            "password": "mypassword"
        })
        assert res.status_code == 200
        data = res.json()
        assert data["message"] == "Login successful"
        assert data["username"] == "loginuser"
        assert "user_id" in data

    def test_login_wrong_password(self, client):
        client.post("/users/register", json={
            "username": "wrongpass",
            "email": "wrongpass@example.com",
            "password": "correctpassword"
        })
        res = client.post("/users/login", params={
            "username": "wrongpass",
            "password": "wrongpassword"
        })
        assert res.status_code == 401

    def test_login_user_not_found(self, client):
        res = client.post("/users/login", params={
            "username": "nobody",
            "password": "nopass"
        })
        assert res.status_code == 404


class TestGetUser:

    def test_get_user_success(self, client):
        reg = client.post("/users/register", json={
            "username": "getuser",
            "email": "getuser@example.com",
            "password": "pass123"
        })
        user_id = reg.json()["id"]
        res = client.get(f"/users/{user_id}")
        assert res.status_code == 200
        assert res.json()["username"] == "getuser"

    def test_get_user_not_found(self, client):
        res = client.get("/users/9999")
        assert res.status_code == 404