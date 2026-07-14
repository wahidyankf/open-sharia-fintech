"""Tests for Example 41: CRUD -- Delete."""

import repository
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_delete_returns_204() -> None:
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    assert response.content == b""  # => co-03: 204 carries no body


def test_delete_actually_removes_the_row() -> None:
    client.delete("/tasks/2")  # => via the HTTP layer
    assert repository.get_task(2) is None  # => bypass HTTP -- confirm it is gone from the DB


def test_delete_missing_id_returns_404() -> None:
    response = client.delete("/tasks/999")  # => never existed in the first place
    assert response.status_code == 404
