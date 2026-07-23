"""Tests for Example 49: Middleware -- Request Logging."""

import logging

import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_request_produces_one_log_line(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="access"):  # => co-16: capture ONLY this logger
        response = client.get("/tasks")
    assert response.status_code == 200
    assert len(caplog.records) == 1  # => exactly one log line for exactly one request
    assert caplog.records[0].message == "GET /tasks -> 200"  # => method + path + status, exactly as the middleware formats it
