"""Tests for Example 30: Validation -- Wrong Type."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_non_numeric_priority_returns_422() -> None:
    response = client.post("/tasks", json={"title": "Buy milk", "priority": "high"})  # => "high" cannot be parsed as an int
    assert response.status_code == 422  # => co-10: rejected before the handler ran
    body = response.json()
    assert body["detail"][0]["loc"] == ["body", "priority"]  # => names the bad field
    assert body["detail"][0]["type"] == "int_parsing"  # => the machine-readable reason


def test_numeric_priority_is_coerced_and_accepted() -> None:
    response = client.post("/tasks", json={"title": "Buy milk", "priority": 3})  # => a genuine int -- passes validation cleanly
    assert response.status_code == 201  # => co-03: created
    assert response.json() == {"title": "Buy milk", "priority": 3}
