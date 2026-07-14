"""Tests for Example 52: A Sanitized 500 Envelope for Unhandled Exceptions."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app, raise_server_exceptions=False)  # => TestClient's default (raise_server_exceptions=True) RE-RAISES the original
# exception into the test even after Starlette sends the handled 500 response over
# the wire -- that default exists so broken handlers fail loudly during development.
# This example is explicitly testing the SANITIZED response a real client receives,
# so it opts out with raise_server_exceptions=False, matching what curl saw for real.


def test_unhandled_exception_returns_sanitized_500() -> None:
    response = client.get("/boom")
    assert response.status_code == 500  # => co-03
    body = response.json()
    assert body == {"error": {"code": "internal_error", "message": "an unexpected error occurred"}}
    assert "RuntimeError" not in response.text  # => co-11: no exception TYPE name leaked
    assert "sensitive" not in response.text  # => co-11: no exception MESSAGE leaked
    assert "Traceback" not in response.text  # => co-11: no stack trace leaked
