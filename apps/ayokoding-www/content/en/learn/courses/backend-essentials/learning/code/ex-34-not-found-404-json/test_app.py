"""Tests for Example 34: A Consistent 404 Envelope Across Methods."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_get_missing_task_returns_envelope() -> None:
    response = client.get("/tasks/404")  # => never seeded
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "task_not_found", "message": "task 404 does not exist"}}


def test_delete_missing_task_returns_same_envelope_shape() -> None:
    response = client.delete("/tasks/404")  # => same missing id, DIFFERENT method
    assert response.status_code == 404  # => co-03: identical status to the GET case
    assert response.json() == {"error": {"code": "task_not_found", "message": "task 404 does not exist"}}  # => co-11: identical BODY shape too -- one envelope, every method, every route


def test_delete_existing_task_succeeds() -> None:
    response = client.delete("/tasks/1")  # => id 1 exists in the in-memory store
    assert response.status_code == 204  # => co-03: no-content success
    assert response.content == b""  # => co-03: 204 carries no body
