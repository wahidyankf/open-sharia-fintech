"""Tests for Example 75: Method Not Allowed."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_delete_on_get_only_path_is_405_with_get_allow() -> None:
    response = client.delete("/tasks")  # => co-02: DELETE was never registered for /tasks
    assert response.status_code == 405  # => co-03: this example's focus
    assert response.headers["allow"] == "GET"  # => co-04, co-03: RFC 9110 SS15.5.6 -- names the ONE method


def test_delete_on_post_only_path_is_405_with_post_allow() -> None:
    response = client.delete("/reports")  # => a DIFFERENT path, DIFFERENT supported method
    assert response.status_code == 405
    assert response.headers["allow"] == "POST"  # => proves Allow reflects the actual path, not a fixed value


def test_registered_methods_still_work_normally() -> None:
    assert client.get("/tasks").status_code == 200  # => contrast: registered methods are unaffected
    assert client.post("/reports").status_code == 200
