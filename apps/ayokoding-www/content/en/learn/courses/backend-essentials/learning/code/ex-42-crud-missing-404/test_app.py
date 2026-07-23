"""Tests for Example 42: CRUD -- Missing Id Returns a 404 Envelope."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

EXPECTED_ENVELOPE = {"error": {"code": "task_not_found", "message": "task 999 does not exist"}}


def test_update_missing_id_returns_envelope() -> None:
    response = client.put("/tasks/999", json={"title": "Nothing to update"})
    assert response.status_code == 404
    assert response.json() == EXPECTED_ENVELOPE


def test_delete_missing_id_returns_same_envelope_shape() -> None:
    response = client.delete("/tasks/999")
    assert response.status_code == 404  # => co-03: identical status to the PUT case
    assert response.json() == EXPECTED_ENVELOPE  # => co-11: identical body shape too
