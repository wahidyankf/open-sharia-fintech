"""Tests for Example 70: Filter Multiple."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_status_alone_returns_eight() -> None:
    response = client.get("/tasks", params={"status": "done"})
    assert len(response.json()) == 8  # => the baseline from Example 69, before combining


def test_status_and_priority_together_narrow_further() -> None:
    response = client.get("/tasks", params={"status": "done", "priority": "high"})  # => co-20: THIS example's focus -- AND semantics, not OR
    body = response.json()
    assert len(body) == 4  # => strictly SMALLER than either single filter alone -- genuine AND narrowing
    assert [t["id"] for t in body] == [5, 11, 17, 23]  # => the exact intersection
    assert all(t["status"] == "done" and t["priority"] == "high" for t in body)  # => BOTH conditions hold
