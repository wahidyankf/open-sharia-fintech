"""Tests for Example 29: Validation -- Required Field."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_missing_title_returns_422() -> None:
    response = client.post("/tasks", json={})  # => body has no "title" at all
    assert response.status_code == 422  # => co-10: rejected before the handler ran
    body = response.json()
    assert body["detail"][0]["loc"] == ["body", "title"]  # => names the missing field
    assert body["detail"][0]["type"] == "missing"  # => the machine-readable reason


def test_valid_title_returns_201() -> None:
    response = client.post("/tasks", json={"title": "Buy milk"})  # => a valid body
    assert response.status_code == 201  # => co-03: created
    assert response.json() == {"title": "Buy milk"}  # => echoed back unchanged
