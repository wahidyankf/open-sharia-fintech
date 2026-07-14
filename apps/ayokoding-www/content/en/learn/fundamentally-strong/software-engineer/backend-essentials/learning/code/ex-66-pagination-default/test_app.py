"""Tests for Example 66: Pagination Default."""

from fastapi.testclient import TestClient

from app import DEFAULT_LIMIT, app

client = TestClient(app)


def test_omitting_limit_uses_the_default_not_the_full_dataset() -> None:
    total = client.get("/tasks/count").json()["total"]  # => confirms 25 rows genuinely exist
    assert total == 25
    response = client.get("/tasks")  # => co-19: THIS example's focus -- no limit param sent at all
    body = response.json()
    assert len(body) == DEFAULT_LIMIT  # => bounded to 10, not the full 25-row table
    assert len(body) < total  # => the default genuinely PROTECTS against an unbounded response


def test_explicit_limit_still_overrides_the_default() -> None:
    response = client.get("/tasks", params={"limit": 3})  # => an explicit value beats the default
    assert len(response.json()) == 3
