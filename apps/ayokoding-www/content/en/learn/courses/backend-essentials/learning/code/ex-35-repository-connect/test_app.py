"""Tests for Example 35: A Repository Module Connected to SQLite."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_list_tasks_returns_seeded_rows() -> None:
    response = client.get("/tasks")  # => reads through repository.list_tasks()
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2  # => the two rows repository.init_db() seeded
    assert body[0] == {"id": 1, "title": "Buy milk"}
    assert body[1] == {"id": 2, "title": "Walk dog"}
