"""Tests for Example 37: CRUD -- Create."""

import repository
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_create_returns_201_with_new_id() -> None:
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "Buy milk"}  # => the first row -> id 1


def test_created_row_actually_persists() -> None:
    client.post("/tasks", json={"title": "Walk dog"})  # => via the HTTP layer, like a real caller
    row = repository.get_task(2)  # => bypass HTTP -- read straight from the DB to prove persistence
    assert row is not None
    assert row["title"] == "Walk dog"
