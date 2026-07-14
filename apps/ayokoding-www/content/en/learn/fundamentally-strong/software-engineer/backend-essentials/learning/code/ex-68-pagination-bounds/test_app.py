"""Tests for Example 68: Pagination Bounds."""

from fastapi.testclient import TestClient

from app import MAX_LIMIT, app

client = TestClient(app)


def test_limit_over_maximum_is_422() -> None:
    response = client.get("/tasks", params={"limit": 1000})  # => co-10: THIS example's named scenario
    assert response.status_code == 422  # => rejected before the handler (and any DB query) ever runs
    detail = response.json()["detail"]
    assert any("limit" in str(err["loc"]) for err in detail)  # => co-11: names the OFFENDING field


def test_limit_at_maximum_is_allowed() -> None:
    response = client.get("/tasks", params={"limit": MAX_LIMIT})  # => the boundary itself is fine
    assert response.status_code == 200  # => the QUERY is valid even though...
    assert len(response.json()) == 25  # => ...only 25 rows exist -- SQL LIMIT just means "at most"


def test_limit_zero_is_422() -> None:
    response = client.get("/tasks", params={"limit": 0})  # => below ge=1, also rejected
    assert response.status_code == 422
