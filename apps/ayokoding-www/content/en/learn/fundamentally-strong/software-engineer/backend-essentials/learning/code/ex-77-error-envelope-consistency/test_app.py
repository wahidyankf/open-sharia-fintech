"""Tests for Example 77: Error Envelope Consistency."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app, raise_server_exceptions=False)  # => co-11: WITHOUT this, TestClient re-raises unhandled exceptions instead of returning the
# => 500 response a real deployed server would send -- this app's own exception_handler(Exception)
# => is exactly what a real uvicorn process relies on to turn that failure into a genuine HTTP response


def _assert_envelope_shape(
    body: dict[str, object],
) -> None:  # => co-11: the ONE check every case shares
    assert "error" in body
    error = body["error"]
    assert isinstance(error, dict)
    assert "code" in error and "message" in error  # => the exact two keys, every time, no exceptions


def test_400_bad_request_uses_the_envelope() -> None:
    response = client.get("/tasks", params={"bad": True})
    assert response.status_code == 400
    _assert_envelope_shape(response.json())


def test_401_unauthorized_uses_the_envelope() -> None:
    response = client.post("/tasks", json={"title": "x"})  # => no Authorization header at all
    assert response.status_code == 401
    _assert_envelope_shape(response.json())


def test_404_not_found_uses_the_envelope() -> None:
    response = client.get("/tasks/999")
    assert response.status_code == 404
    _assert_envelope_shape(response.json())


def test_422_validation_error_uses_the_envelope() -> None:
    response = client.post("/tasks", json={}, headers={"Authorization": "Bearer s3cr3t-token-abc123"})  # => title omitted -- co-10 validation failure, still wrapped in the SAME shape
    assert response.status_code == 422
    _assert_envelope_shape(response.json())


def test_500_internal_error_uses_the_envelope_and_hides_details() -> None:
    response = client.get("/boom", headers={})
    assert response.status_code == 500
    body = response.json()
    _assert_envelope_shape(body)
    assert "RuntimeError" not in body["error"]["message"]  # => co-11: the real exception never leaks


def test_every_error_status_code_shares_the_identical_top_level_keys() -> None:
    codes_and_responses = [
        client.get("/tasks", params={"bad": True}),
        client.post("/tasks", json={"title": "x"}),
        client.get("/tasks/999"),
        client.post("/tasks", json={}, headers={"Authorization": "Bearer s3cr3t-token-abc123"}),
        client.get("/boom"),
    ]
    for response in codes_and_responses:  # => co-11: THIS example's core claim -- verified across all five
        assert set(response.json().keys()) == {"error"}  # => never "detail", never a bare string
