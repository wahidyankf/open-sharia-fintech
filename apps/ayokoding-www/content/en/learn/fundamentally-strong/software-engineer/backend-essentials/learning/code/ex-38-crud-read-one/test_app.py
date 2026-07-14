"""Tests for Example 38: CRUD -- Read One."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_read_existing_task() -> None:
    response = client.get("/tasks/2")  # => "Walk dog", seeded second
    assert response.status_code == 200
    assert response.json() == {"id": 2, "title": "Walk dog"}


def test_read_missing_task_returns_404() -> None:
    response = client.get("/tasks/999")  # => never seeded
    assert response.status_code == 404
