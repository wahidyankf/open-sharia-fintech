"""Tests for Example 63: Protect Writes Only."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_get_is_open_without_any_token() -> None:
    response = client.get("/items")  # => co-02: no Authorization header sent at all
    assert response.status_code == 200  # => reads never required a token
    assert response.json() == {"1": "milk", "2": "bread"}


def test_post_without_token_is_401() -> None:
    response = client.post("/items", params={"name": "eggs"})  # => a WRITE, no token
    assert response.status_code == 401  # => co-18: the read/write split blocks this


def test_post_with_token_succeeds() -> None:
    response = client.post(
        "/items",
        params={"name": "eggs"},
        headers={"Authorization": "Bearer s3cr3t-token-abc123"},
    )
    assert response.status_code == 200  # => co-18: a valid token unlocks the write
    assert response.json()["name"] == "eggs"


def test_delete_without_token_is_401_but_get_still_open() -> None:
    assert client.delete("/items/1").status_code == 401  # => another write, still guarded
    assert client.get("/items").status_code == 200  # => reads remain unaffected by the write guard
