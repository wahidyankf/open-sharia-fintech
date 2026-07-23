"""Tests for Example 33: A Domain Exception Handler."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_existing_task_returns_200() -> None:
    response = client.get("/tasks/1")  # => id 1 exists in the in-memory store
    assert response.status_code == 200
    assert response.json() == {"title": "Buy milk"}


def test_missing_task_returns_mapped_404() -> None:
    response = client.get("/tasks/99")  # => id 99 was never seeded
    assert response.status_code == 404  # => TaskNotFoundError -> 404, via the handler
    assert response.json() == {"error": {"code": "task_not_found", "message": "task 99 does not exist"}}
