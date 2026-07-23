"""Tests for Example 73: Combined List Query."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_filter_alone_reports_the_filtered_total() -> None:
    response = client.get("/tasks", params={"status": "done", "limit": 50})
    body = response.json()
    assert body["total"] == 8  # => co-19: total is the FILTERED count, not 25


def test_filter_plus_pagination_plus_sort_all_compose() -> None:
    response = client.get(  # => co-19, co-20: this example's focus -- three features, one call
        "/tasks",
        params={"status": "done", "limit": 3, "offset": 0, "sort": "-created_at"},
    )
    body = response.json()
    assert body["total"] == 8  # => the FILTERED total (status=done), unaffected by pagination
    assert len(body["items"]) == 3  # => the PAGE size, honoring limit
    assert [t["id"] for t in body["items"]] == [
        23,
        20,
        17,
    ]  # => the 3 NEWEST done tasks, descending
    assert body["next"] == 3  # => co-19: a further page exists (8 - 3 = 5 remaining)


def test_second_page_of_the_same_filtered_sorted_query() -> None:
    response = client.get(
        "/tasks",
        params={"status": "done", "limit": 3, "offset": 3, "sort": "-created_at"},
    )
    body = response.json()
    assert [t["id"] for t in body["items"]] == [
        14,
        11,
        8,
    ]  # => continues where the first page left off
