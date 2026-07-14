"""Tests for Example 50: Middleware -- Timing Header."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_response_carries_a_parseable_timing_header() -> None:
    response = client.get("/tasks")
    assert response.status_code == 200
    elapsed = float(response.headers["X-Process-Time"])  # => co-04: must parse as a real number
    assert elapsed >= 0.0  # => co-16: elapsed time can never be negative
