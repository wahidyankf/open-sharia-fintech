"""Tests for Example 69: Filter by Field."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_no_filter_returns_all_twenty_five() -> None:
    response = client.get("/tasks")  # => co-20: baseline -- the UNFILTERED full list
    assert len(response.json()) == 25


def test_status_done_returns_only_eight_matching_rows() -> None:
    response = client.get("/tasks", params={"status": "done"})  # => co-20: this example's named scenario
    body = response.json()
    assert len(body) == 8  # => a GENUINELY smaller subset than the full 25 -- not a toy 1-row dataset
    assert all(t["status"] == "done" for t in body)  # => every returned row actually matches the filter
    assert [t["id"] for t in body] == [
        2,
        5,
        8,
        11,
        14,
        17,
        20,
        23,
    ]  # => the exact expected ids


def test_status_with_no_matches_returns_empty() -> None:
    response = client.get("/tasks", params={"status": "archived"})  # => a value that matches nothing
    assert response.json() == []  # => an empty list, not an error -- filtering degrades gracefully
