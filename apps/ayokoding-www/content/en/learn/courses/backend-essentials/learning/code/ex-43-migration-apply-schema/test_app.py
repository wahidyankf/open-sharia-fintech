"""Tests for Example 43: Apply a schema.sql Migration at Startup."""

import repository
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_table_exists_after_migration() -> None:
    assert repository.table_exists("tasks") is True  # => co-15: the direct, low-level check


def test_health_endpoint_confirms_readiness() -> None:
    response = client.get("/health")  # => the HTTP-level view of the same fact
    assert response.status_code == 200
    assert response.json() == {"tasks_table_ready": True}
