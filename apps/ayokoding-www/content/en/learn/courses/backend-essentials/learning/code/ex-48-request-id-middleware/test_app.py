"""Tests for Example 48: Middleware -- X-Request-Id."""

import uuid

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_response_carries_a_well_formed_request_id() -> None:
    response = client.get("/tasks")
    assert response.status_code == 200
    request_id = response.headers["X-Request-Id"]  # => co-04: present on every response
    uuid.UUID(request_id)  # => raises ValueError if it is not a real UUID -- it is not


def test_two_requests_get_two_different_request_ids() -> None:
    first = client.get("/tasks").headers["X-Request-Id"]
    second = client.get("/tasks").headers["X-Request-Id"]
    assert first != second  # => co-16: the middleware runs FRESH for every request
