"""Tests for Example 74: Idempotent PUT, Verified."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

BODY = {
    "title": "write the report",
    "status": "in_progress",
}  # => the SAME body used for both PUT calls


def test_first_put_replaces_the_resource() -> None:
    response = client.put("/tasks/1", json=BODY)
    assert response.status_code == 200
    assert response.json() == {"id": 1, **BODY}


def test_second_identical_put_produces_the_same_state_and_no_duplicate() -> None:
    first = client.put("/tasks/1", json=BODY)  # => co-02: apply the SAME PUT again
    second = client.put("/tasks/1", json=BODY)  # => co-02: THIS example's focus -- a repeated PUT
    assert first.json() == second.json()  # => byte-identical response -- the resource state did not change
    total = client.get("/tasks/count").json()["total"]
    assert total == 1  # => co-02: still exactly ONE row -- PUT never inserted a duplicate


def test_put_missing_id_is_404() -> None:
    response = client.put("/tasks/999", json=BODY)
    assert response.status_code == 404  # => co-03: this example only replaces, never auto-creates
