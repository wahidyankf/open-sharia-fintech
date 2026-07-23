"""Tests for Example 51: Middleware -- CORS."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_allowed_origin_gets_cors_header() -> None:
    response = client.get("/tasks", headers={"Origin": "https://example.com"})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://example.com"  # => co-04/co-16: the header CORSMiddleware adds for a matching origin


def test_disallowed_origin_gets_no_cors_header() -> None:
    response = client.get("/tasks", headers={"Origin": "https://evil.example"})
    assert response.status_code == 200  # => the request still succeeds...
    assert "access-control-allow-origin" not in response.headers  # => ...but WITHOUT the header, so a browser blocks the response from being read
