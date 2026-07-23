"""Tests for Example 60: Missing Token."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_no_authorization_header_is_401_with_missing_message() -> None:
    response = client.get("/protected")  # => co-18: header omitted entirely, the case this example names
    assert response.status_code == 401
    body = response.json()
    assert body["error"]["code"] == "unauthorized"  # => co-11: consistent envelope shape
    assert "missing" in body["error"]["message"]  # => the specific reason distinguishes this from ex-61


def test_valid_token_still_reaches_handler_for_contrast() -> None:
    response = client.get("/protected", headers={"Authorization": "Bearer s3cr3t-token-abc123"})
    assert response.status_code == 200  # => contrast case: proves the dependency isn't just always-fail
    assert response.json() == {"user": "alice"}
