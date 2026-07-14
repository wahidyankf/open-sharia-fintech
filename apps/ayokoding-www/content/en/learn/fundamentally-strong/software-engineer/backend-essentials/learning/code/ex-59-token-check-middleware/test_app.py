"""Tests for Example 59: Token-Check Middleware."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_public_route_needs_no_token() -> None:
    response = client.get("/public")  # => never passes through the token branch
    assert response.status_code == 200
    assert response.json() == {"access": "public"}


def test_protected_route_with_valid_token_reaches_handler() -> None:
    response = client.get("/protected/data", headers={"Authorization": "Bearer s3cr3t-token-abc123"})
    assert response.status_code == 200  # => co-16: middleware let the request through
    assert response.json()["user"] == "alice"  # => request.state.user, set by the middleware


def test_protected_route_without_token_is_401() -> None:
    response = client.get("/protected/data")  # => no Authorization header at all
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"  # => co-11: structured envelope shape
