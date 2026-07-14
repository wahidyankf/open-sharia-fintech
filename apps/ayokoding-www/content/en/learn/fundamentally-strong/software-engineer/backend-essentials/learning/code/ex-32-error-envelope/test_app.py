"""Tests for Example 32: A Custom Error Envelope."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_missing_title_returns_custom_envelope() -> None:
    response = client.post("/tasks", json={})  # => triggers the same validation failure as ex-29
    assert response.status_code == 422  # => co-03: status is unchanged
    assert response.json() == {"error": {"code": "validation_error", "message": "title: Field required"}}  # => co-11: but the BODY now uses the custom envelope, not FastAPI's default shape


def test_valid_body_is_unaffected() -> None:
    response = client.post("/tasks", json={"title": "Buy milk"})  # => the happy path
    assert response.status_code == 201  # => the override only touches the FAILURE path
    assert response.json() == {"title": "Buy milk"}  # => the custom envelope only wraps FAILURES
