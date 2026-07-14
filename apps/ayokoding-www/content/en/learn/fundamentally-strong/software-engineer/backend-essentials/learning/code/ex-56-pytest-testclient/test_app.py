"""Tests for Example 56: pytest + FastAPI's TestClient."""

# => co-22: the fixture below is the WHOLE point of this example -- every
#    test function receives a freshly reset TestClient, never a shared one
from collections.abc import Iterator  # => the precise return type a generator fixture needs

import pytest  # => co-22: pytest's own fixture/test discovery machinery
import repository  # => co-14: the module whose init_db() resets state per test
from fastapi.testclient import TestClient  # => co-22: drives the ASGI app without a real socket

from app import app  # => the SAME FastAPI instance uvicorn would otherwise serve


@pytest.fixture()  # => co-22: pytest calls this ONCE PER TEST FUNCTION that requests it
def client() -> Iterator[TestClient]:  # => a generator fixture -- code after yield is teardown
    # => co-22: TestClient drives the ASGI app IN-PROCESS -- no uvicorn, no real
    #    socket, no network round trip -- yet it exercises the exact same FastAPI
    #    routing/validation/middleware stack a real HTTP request would go through
    repository.init_db()  # => a FRESH database before every single test function
    with TestClient(app) as test_client:  # => "with" also runs startup/shutdown events
        yield test_client  # => each test function receives THIS client as its argument


def test_create_task_returns_201(client: TestClient) -> None:  # => "client" is the fixture above
    response = client.post("/tasks", json={"title": "Buy milk"})  # => in-process POST, no curl needed
    assert response.status_code == 201  # => co-03: matches the app's status_code=201 decorator arg
    assert response.json()["title"] == "Buy milk"  # => the body round-trips through real validation


def test_list_tasks_reflects_created_tasks(client: TestClient) -> None:  # => a fresh client, again
    client.post("/tasks", json={"title": "Buy milk"})  # => grows the list this test's own client sees
    client.post("/tasks", json={"title": "Walk dog"})  # => a second row, same isolated database
    response = client.get("/tasks")  # => reads back everything this test itself just wrote
    assert response.status_code == 200  # => the plain success case
    titles = [task["title"] for task in response.json()]  # => extracts just the field being asserted
    assert titles == ["Buy milk", "Walk dog"]  # => insertion order, proven end to end


def test_each_test_gets_an_isolated_database(client: TestClient) -> None:  # => the ISOLATION proof
    # => proves the fixture's repository.init_db() call genuinely resets state --
    #    if a previous test's rows had leaked in, this list would NOT be empty
    response = client.get("/tasks")  # => runs AFTER the two tests above, in whatever order pytest picks
    assert response.status_code == 200  # => the endpoint itself never fails
    assert response.json() == []  # => this test creates nothing, so the list starts empty
