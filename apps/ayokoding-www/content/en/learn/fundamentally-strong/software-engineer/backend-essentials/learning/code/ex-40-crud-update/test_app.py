"""Tests for Example 40: CRUD -- Update."""

import repository
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_update_returns_200_with_new_title() -> None:
    response = client.put("/tasks/1", json={"title": "Buy oat milk"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Buy oat milk"}


def test_update_actually_persists() -> None:
    client.put("/tasks/2", json={"title": "Walk the dog twice"})  # => via the HTTP layer
    row = repository.get_task(2)  # => bypass HTTP -- confirm the change reached the DB file
    assert row is not None
    assert row["title"] == "Walk the dog twice"


def test_update_missing_id_returns_404() -> None:
    response = client.put("/tasks/999", json={"title": "Nothing to update"})
    assert response.status_code == 404
