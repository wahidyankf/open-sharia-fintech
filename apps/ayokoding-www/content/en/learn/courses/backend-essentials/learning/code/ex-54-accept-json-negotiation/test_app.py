"""Tests for Example 54: Hand-Written Accept Header Negotiation."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_explicit_json_accept_is_allowed() -> None:
    response = client.get("/tasks", headers={"Accept": "application/json"})
    assert response.status_code == 200


def test_wildcard_accept_is_allowed() -> None:
    response = client.get("/tasks", headers={"Accept": "*/*"})  # => e.g. curl's own default
    assert response.status_code == 200


def test_unsupported_accept_is_rejected_with_406() -> None:
    response = client.get("/tasks", headers={"Accept": "text/plain"})
    assert response.status_code == 406  # => co-21: hand-written, unlike the built-in 422
    assert response.json() == {"detail": "only application/json is supported"}
