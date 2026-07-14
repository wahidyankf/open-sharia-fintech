"""Tests for Example 80: Stateless, Two Workers (in-process TestClient half)."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)  # => a single in-process client, exercising the SAME statelessness contract
# => the paired shell script (two_workers.sh) proves the SAME contract with TWO REAL OS processes


def test_create_then_read_round_trips_through_the_db_alone() -> None:
    created = client.post("/tasks", json={"title": "shared state proof"})
    assert created.status_code == 201
    task_id = created.json()["id"]
    read = client.get(f"/tasks/{task_id}")  # => co-05: no in-process cache is involved -- pure DB read
    assert read.status_code == 200
    assert read.json()["title"] == "shared state proof"


def test_reading_an_unknown_id_is_404_not_a_crash() -> None:
    response = client.get("/tasks/999999")  # => co-05: statelessness means no worker "remembers" anything
    assert response.status_code == 404  # => extra beyond what's in the DB itself
