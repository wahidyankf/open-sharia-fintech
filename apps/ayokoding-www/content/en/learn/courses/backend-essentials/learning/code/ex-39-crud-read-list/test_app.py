"""Tests for Example 39: CRUD -- Read List."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_list_starts_empty() -> None:
    response = client.get("/tasks")  # => nothing created yet in THIS test
    assert response.status_code == 200
    assert response.json() == []


def test_list_grows_as_tasks_are_created() -> None:
    client.post("/tasks", json={"title": "Buy milk"})
    client.post("/tasks", json={"title": "Walk dog"})
    response = client.get("/tasks")  # => co-14: the array now reflects BOTH creates
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Buy milk"},
        {"id": 2, "title": "Walk dog"},
    ]  # => test_list_starts_empty ran first and inserted nothing, so ids start at 1
