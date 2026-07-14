"""Tests for Example 45: A Repository That Returns Typed Rows."""

from fastapi.testclient import TestClient

from app import app
from repository import TaskRow

client = TestClient(app)


def test_typed_row_shape_is_preserved_over_json() -> None:
    row: TaskRow = TaskRow(id=1, title="Buy milk")  # => construct one directly, like the type checker sees it
    assert row["id"] == 1
    assert row["title"] == "Buy milk"


def test_endpoint_returns_typed_rows_as_json() -> None:
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Buy milk"},
        {"id": 2, "title": "Walk dog"},
    ]  # => TypedDict serializes exactly like a plain dict over the wire
