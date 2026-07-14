"""Tests for Example 57: Sessions vs Tokens."""

from fastapi.testclient import (
    TestClient,
)  # => co-22: exercises the ASGI app in-process, no socket

from app import app  # => the SAME app object curl hits when served by uvicorn

client = TestClient(app)  # => wraps app in a requests-like interface for assertions


def test_session_login_sets_cookie_and_profile_reads_it() -> None:
    login = client.post("/login-session")  # => step 1: obtain a session cookie
    assert login.status_code == 200  # => co-03: issuance succeeds
    assert "session_id" in login.cookies  # => co-04: the cookie is genuinely present on the response
    profile = client.get("/profile-session")  # => TestClient reuses cookies across calls automatically
    assert profile.status_code == 200  # => the SAME client (with cookie) is recognized
    assert profile.json()["username"] == "alice"  # => identity resolved via server-side session state


def test_profile_session_without_cookie_is_401() -> None:
    fresh_client = TestClient(app)  # => a brand-new client -- no cookie has ever been set here
    response = fresh_client.get("/profile-session")
    assert response.status_code == 401  # => co-03: no session, no identity, unauthenticated


def test_token_login_and_profile_identify_caller() -> None:
    login = client.post("/login-token")  # => step 1: obtain the token itself (no cookie involved)
    token = login.json()["token"]  # => the CLIENT now holds the entire credential
    response = client.get("/profile-token", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # => resolved purely from the header, no lookup table needed
    assert response.json()["username"] == "alice"  # => same identity, different mechanism


def test_profile_token_without_header_is_401() -> None:
    response = client.get("/profile-token")  # => no Authorization header at all
    assert response.status_code == 401  # => co-03: missing credential, same failure mode as sessions
