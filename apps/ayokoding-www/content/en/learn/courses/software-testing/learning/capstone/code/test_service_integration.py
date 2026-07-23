"""Capstone Step 4: an integration test hitting app.py's real HTTP endpoints with TestClient."""
# Drives the SAME service.py logic Steps 1-3 already verified in isolation, now reached through
# a real FastAPI app and a real (in-process) HTTP boundary -- exactly the integration tier this
# capstone's pyramid needed. See the capstone overview's Run block for the coverage report read
# from `pytest --cov` across ALL FOUR test files together.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from app import app  # => co-23: the REAL, running FastAPI app -- not a mock of it  # fmt: skip
from fastapi.testclient import TestClient  # => co-23: drives the real app in-process, no real socket  # fmt: skip

client = TestClient(app)  # => co-23: drives the REAL, running app -- no mocking of app.py itself  # fmt: skip


def test_integration_add_item_then_read_total() -> None:  # => co-23: the full HTTP round trip  # fmt: skip
    add_response = client.post("/orders/order-cap-1/items", json={"price": 12.50})  # => a REAL POST  # fmt: skip
    assert add_response.status_code == 200  # => co-23: the REAL handler's status code  # fmt: skip
    assert add_response.json() == {"order_id": "order-cap-1", "item_count": 1}  # => co-23: real body  # fmt: skip

    add_second = client.post("/orders/order-cap-1/items", json={"price": 7.50})  # => a SECOND real POST  # fmt: skip
    assert add_second.status_code == 200  # => co-23: still a real, successful response  # fmt: skip
    assert add_second.json()["item_count"] == 2  # => co-23: state accumulates ACROSS real requests  # fmt: skip

    total_response = client.get("/orders/order-cap-1/total")  # => a REAL GET, reading real state  # fmt: skip
    assert total_response.status_code == 200  # => co-23: the real read succeeded  # fmt: skip
    assert total_response.json() == {"order_id": "order-cap-1", "total": 20.0}  # => 12.50 + 7.50  # fmt: skip


def test_integration_total_for_unknown_order_is_zero() -> None:  # => co-23: a REAL empty-state path  # fmt: skip
    response = client.get("/orders/never-created/total")  # => an order id that genuinely never existed  # fmt: skip
    assert response.status_code == 200  # => co-23: still a real, successful (not 404) response  # fmt: skip
    assert response.json() == {"order_id": "never-created", "total": 0}  # => co-23: genuinely empty  # fmt: skip
