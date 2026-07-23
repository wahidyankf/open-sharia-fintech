"""Tests for Example 78: curl CRUD + Auth Script."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

AUTH = {"Authorization": "Bearer s3cr3t-token-abc123"}


def test_create_without_token_is_401() -> None:
    response = client.post("/tasks", json={"title": "write the report"})
    assert response.status_code == 401


def test_full_crud_round_trip_with_token() -> None:  # => mirrors the companion shell script step for step
    created = client.post("/tasks", json={"title": "write the report"}, headers=AUTH)
    assert created.status_code == 201
    task_id = created.json()["id"]

    read = client.get(f"/tasks/{task_id}")  # => reads need no token
    assert read.status_code == 200
    assert read.json()["title"] == "write the report"

    updated = client.put(
        f"/tasks/{task_id}",
        json={"title": "write the report", "status": "done"},
        headers=AUTH,
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "done"

    deleted = client.delete(f"/tasks/{task_id}", headers=AUTH)
    assert deleted.status_code == 204

    after_delete = client.get(f"/tasks/{task_id}")
    assert after_delete.status_code == 404  # => genuinely gone
