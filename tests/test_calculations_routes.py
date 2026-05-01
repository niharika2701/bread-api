import pytest


class TestAddCalculation:

    def test_add_success(self, client):
        res = client.post("/calculations/", json={
            "a": 10, "b": 5, "type": "Add"
        })
        assert res.status_code == 201
        data = res.json()
        assert data["result"] == 15.0
        assert data["type"] == "Add"
        assert "id" in data
        assert "created_at" in data

    def test_subtract_success(self, client):
        res = client.post("/calculations/", json={
            "a": 20, "b": 8, "type": "Sub"
        })
        assert res.status_code == 201
        assert res.json()["result"] == 12.0

    def test_multiply_success(self, client):
        res = client.post("/calculations/", json={
            "a": 6, "b": 7, "type": "Multiply"
        })
        assert res.status_code == 201
        assert res.json()["result"] == 42.0

    def test_divide_success(self, client):
        res = client.post("/calculations/", json={
            "a": 100, "b": 4, "type": "Divide"
        })
        assert res.status_code == 201
        assert res.json()["result"] == 25.0

    def test_divide_by_zero_rejected(self, client):
        res = client.post("/calculations/", json={
            "a": 10, "b": 0, "type": "Divide"
        })
        assert res.status_code == 400

    def test_invalid_type_rejected(self, client):
        res = client.post("/calculations/", json={
            "a": 1, "b": 2, "type": "Power"
        })
        assert res.status_code == 400

    def test_add_with_user_id(self, client):
        user = client.post("/users/register", json={
            "username": "calcuser",
            "email": "calcuser@example.com",
            "password": "pass123"
        })
        user_id = user.json()["id"]
        res = client.post("/calculations/", json={
            "a": 3, "b": 3, "type": "Add", "user_id": user_id
        })
        assert res.status_code == 201
        assert res.json()["user_id"] == user_id

    def test_invalid_user_id_rejected(self, client):
        res = client.post("/calculations/", json={
            "a": 1, "b": 2, "type": "Add", "user_id": 9999
        })
        assert res.status_code == 404


class TestBrowseCalculations:

    def test_browse_returns_list(self, client):
        client.post("/calculations/", json={"a": 1, "b": 2, "type": "Add"})
        client.post("/calculations/", json={"a": 3, "b": 4, "type": "Multiply"})
        res = client.get("/calculations/")
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert len(res.json()) >= 2

    def test_browse_empty(self, client):
        res = client.get("/calculations/")
        assert res.status_code == 200
        assert res.json() == []


class TestReadCalculation:

    def test_read_success(self, client):
        post = client.post("/calculations/", json={
            "a": 9, "b": 3, "type": "Divide"
        })
        calc_id = post.json()["id"]
        res = client.get(f"/calculations/{calc_id}")
        assert res.status_code == 200
        assert res.json()["result"] == 3.0

    def test_read_not_found(self, client):
        res = client.get("/calculations/9999")
        assert res.status_code == 404


class TestEditCalculation:

    def test_edit_success(self, client):
        post = client.post("/calculations/", json={
            "a": 2, "b": 3, "type": "Add"
        })
        calc_id = post.json()["id"]
        res = client.put(f"/calculations/{calc_id}", json={
            "a": 10, "b": 5, "type": "Multiply"
        })
        assert res.status_code == 200
        data = res.json()
        assert data["result"] == 50.0
        assert data["type"] == "Multiply"

    def test_edit_not_found(self, client):
        res = client.put("/calculations/9999", json={
            "a": 1, "b": 2, "type": "Add"
        })
        assert res.status_code == 404

    def test_edit_invalid_type(self, client):
        post = client.post("/calculations/", json={
            "a": 2, "b": 3, "type": "Add"
        })
        calc_id = post.json()["id"]
        res = client.put(f"/calculations/{calc_id}", json={
            "a": 1, "b": 2, "type": "InvalidOp"
        })
        assert res.status_code == 400


class TestDeleteCalculation:

    def test_delete_success(self, client):
        post = client.post("/calculations/", json={
            "a": 5, "b": 5, "type": "Add"
        })
        calc_id = post.json()["id"]
        res = client.delete(f"/calculations/{calc_id}")
        assert res.status_code == 204
        # Confirm it's gone
        res = client.get(f"/calculations/{calc_id}")
        assert res.status_code == 404

    def test_delete_not_found(self, client):
        res = client.delete("/calculations/9999")
        assert res.status_code == 404