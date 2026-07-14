"""Tests for Example 55: Create Then Read -- A Persisted Round Trip."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_create_then_read_round_trip() -> None:
    create_response = client.post("/tasks", json={"title": "Buy milk"})  # => step 1: create
    assert create_response.status_code == 201
    created_id = create_response.json()["id"]

    read_response = client.get(f"/tasks/{created_id}")  # => step 2: read the SAME id back
    assert read_response.status_code == 200
    assert read_response.json() == {
        "id": created_id,
        "title": "Buy milk",
    }  # => co-14: the round trip proves the POST reached durable storage, not just memory
