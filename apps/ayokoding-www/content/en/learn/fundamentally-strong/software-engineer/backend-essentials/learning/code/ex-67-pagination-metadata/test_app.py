"""Tests for Example 67: Pagination Metadata."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_first_page_reports_total_and_a_next_offset() -> None:
    response = client.get("/tasks", params={"limit": 10, "offset": 0})
    body = response.json()
    assert body["total"] == 25  # => co-19: the WHOLE table's size, not just this page's length
    assert len(body["items"]) == 10
    assert body["next"] == 10  # => co-19: exactly where the next page should start


def test_last_page_reports_next_as_null() -> None:
    response = client.get("/tasks", params={"limit": 10, "offset": 20})  # => rows 21..25, only 5 left
    body = response.json()
    assert len(body["items"]) == 5  # => fewer than the requested limit -- genuinely the last page
    assert body["next"] is None  # => co-19: the sentinel that says "nothing more to fetch"
