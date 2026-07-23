"""Tests for Example 36: Parameterized Queries Neutralize Injection."""

import repository
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_normal_search_matches_a_row() -> None:
    response = client.get("/tasks/search", params={"title": "milk"})  # => a normal substring
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "title": "Buy milk"}]


def test_injection_attempt_matches_nothing_and_table_survives() -> None:
    payload = "'; DROP TABLE tasks; --"  # => a classic injection payload, sent as ORDINARY data
    response = client.get("/tasks/search", params={"title": payload})
    assert response.status_code == 200  # => co-14: no SQL error -- the payload was never SQL
    assert response.json() == []  # => no title CONTAINS that literal string, so zero matches
    assert repository.count_tasks() == 2  # => co-20: the table itself is completely untouched
