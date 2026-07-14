"""Tests for Example 53: The 422 Detail Array Lists Every Offending Field."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_single_violation_yields_one_detail_entry() -> None:
    response = client.post("/tasks", json={"title": "Buy milk", "priority": -1})
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert len(detail) == 1  # => only "priority" is wrong here
    assert detail[0]["loc"] == ["body", "priority"]


def test_two_simultaneous_violations_yield_two_detail_entries() -> None:
    response = client.post("/tasks", json={"title": "", "priority": -1})  # => BOTH fail at once
    assert response.status_code == 422  # => co-03: still a single 422, not two responses
    detail = response.json()["detail"]  # => co-10/co-11: the ARRAY lists BOTH offenders
    assert len(detail) == 2
    fields = {entry["loc"][-1] for entry in detail}
    assert fields == {
        "title",
        "priority",
    }  # => every violated field is individually named
