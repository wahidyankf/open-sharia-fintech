"""Tests for Example 58: Issue a Token."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_login_with_correct_credentials_returns_token() -> None:
    response = client.post("/login", json={"username": "alice", "password": "wonderland"})
    assert response.status_code == 200  # => co-03: a successful login
    body = response.json()
    assert body["token"] == "s3cr3t-token-abc123"  # => the exact token string is present in the body


def test_login_with_wrong_password_is_401() -> None:
    response = client.post("/login", json={"username": "alice", "password": "wrong"})
    assert response.status_code == 401  # => co-03: rejected before any token is issued
    assert "token" not in response.json()  # => no partial/leaked credential on failure


def test_login_missing_field_is_422() -> None:
    response = client.post("/login", json={"username": "alice"})  # => password omitted entirely
    assert response.status_code == 422  # => co-10: Pydantic validation runs BEFORE handler logic
