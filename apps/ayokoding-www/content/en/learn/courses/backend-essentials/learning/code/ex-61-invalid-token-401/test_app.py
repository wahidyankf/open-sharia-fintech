"""Tests for Example 61: Invalid Token."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_malformed_token_is_401_with_invalid_message() -> None:
    response = client.get("/protected", headers={"Authorization": "Bearer not-a-real-token"})  # => co-18: a WELL-FORMED header, wrong value -- this example's named scenario
    assert response.status_code == 401
    body = response.json()
    assert body["error"]["message"] == "token is invalid"  # => distinct message from the missing case


def test_valid_token_still_reaches_handler_for_contrast() -> None:
    response = client.get("/protected", headers={"Authorization": "Bearer s3cr3t-token-abc123"})
    assert response.status_code == 200
    assert response.json() == {"user": "alice"}
