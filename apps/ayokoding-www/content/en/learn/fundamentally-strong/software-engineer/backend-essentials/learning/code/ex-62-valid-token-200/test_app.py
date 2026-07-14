"""Tests for Example 62: Valid Token."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_valid_token_returns_200_and_grants_access() -> None:
    response = client.get("/protected", headers={"Authorization": "Bearer s3cr3t-token-abc123"})  # => co-18: exactly the right credential -- this example's named scenario
    assert response.status_code == 200
    assert response.json() == {"user": "alice", "granted": True}


def test_missing_and_invalid_still_fail_for_contrast() -> None:
    assert client.get("/protected").status_code == 401  # => no header at all
    assert client.get("/protected", headers={"Authorization": "Bearer wrong"}).status_code == 401  # => header present, value wrong
