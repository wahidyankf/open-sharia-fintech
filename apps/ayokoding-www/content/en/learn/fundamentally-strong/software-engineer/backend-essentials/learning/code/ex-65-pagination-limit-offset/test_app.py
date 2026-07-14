"""Tests for Example 65: Pagination limit/offset."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)  # => the 25-row seeded dataset is already in place by the time this imports


def test_default_page_returns_first_ten() -> None:
    response = client.get("/tasks")  # => co-19: no params -- uses the handler's own defaults
    body = response.json()
    assert response.status_code == 200
    assert len(body) == 10  # => the default limit, not all 25 rows
    assert [t["id"] for t in body] == list(range(1, 11))  # => the FIRST page, ids 1..10


def test_limit_5_offset_10_returns_a_different_window() -> None:
    response = client.get("/tasks", params={"limit": 5, "offset": 10})  # => co-19: this example's focus
    body = response.json()
    assert len(body) == 5  # => exactly 5 rows, not 25 and not 10
    assert [t["id"] for t in body] == [
        11,
        12,
        13,
        14,
        15,
    ]  # => a GENUINELY different slice than the default


def test_offset_past_the_end_returns_empty() -> None:
    response = client.get("/tasks", params={"limit": 10, "offset": 100})  # => beyond the 25 seeded rows
    assert response.json() == []  # => no error, just an empty page -- SQL LIMIT/OFFSET degrade gracefully
