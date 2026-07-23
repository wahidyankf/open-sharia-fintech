"""Tests for Example 64: Session-Cookie Auth."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)  # => TestClient persists cookies across calls, like a real browser session


def test_login_sets_cookie_and_me_reads_it_back() -> None:
    login = client.post("/login", params={"username": "alice", "password": "wonderland"})
    assert login.status_code == 200
    assert "session_id" in login.cookies  # => co-04: the Set-Cookie genuinely landed on this client
    me = client.get("/me")  # => the cookie set above is sent AUTOMATICALLY on this next request
    assert me.status_code == 200
    assert me.json() == {"username": "alice"}


def test_me_without_prior_login_is_401() -> None:
    fresh_client = TestClient(app)  # => a brand-new client, no cookie jar populated at all
    response = fresh_client.get("/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


def test_login_with_wrong_password_never_sets_a_cookie() -> None:
    fresh_client = TestClient(app)
    response = fresh_client.post("/login", params={"username": "alice", "password": "wrong"})
    assert response.status_code == 401
    assert "session_id" not in response.cookies  # => a failed login must never establish a session
