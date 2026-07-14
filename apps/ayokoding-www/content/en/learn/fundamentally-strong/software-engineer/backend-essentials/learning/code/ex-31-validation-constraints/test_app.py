"""Tests for Example 31: Validation -- Field Constraints."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_empty_title_rejected() -> None:
    response = client.post("/tasks", json={"title": "", "priority": 1})  # => title too short
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_too_short"  # => min_length=1 violated


def test_zero_priority_rejected() -> None:
    response = client.post("/tasks", json={"title": "Buy milk", "priority": 0})  # => priority must be > 0, not >= 0
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "greater_than"  # => gt=0 violated


def test_valid_body_accepted() -> None:
    response = client.post("/tasks", json={"title": "Buy milk", "priority": 1})  # => both satisfied
    assert response.status_code == 201
    assert response.json() == {"title": "Buy milk", "priority": 1}
