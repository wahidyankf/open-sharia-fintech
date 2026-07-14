"""Tests for Example 72: Sort Param."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_ascending_sort_starts_at_id_1() -> None:
    response = client.get("/tasks", params={"sort": "created_at"})  # => the default direction
    body = response.json()
    assert body[0]["id"] == 1  # => the OLDEST created_at first
    assert body[-1]["id"] == 25  # => the newest last


def test_descending_sort_reverses_the_order() -> None:
    response = client.get("/tasks", params={"sort": "-created_at"})  # => co-20: this example's focus
    body = response.json()
    assert body[0]["id"] == 25  # => the NEWEST created_at first -- a genuinely different order than ascending
    assert body[-1]["id"] == 1
    assert len(body) == 25  # => same 25 rows, only the ORDER changed -- sort never filters


def test_invalid_sort_value_is_422() -> None:
    response = client.get("/tasks", params={"sort": "title"})  # => not in the allowed Literal set
    assert response.status_code == 422  # => co-10: rejected by the closed Literal type, not by hand-written code
