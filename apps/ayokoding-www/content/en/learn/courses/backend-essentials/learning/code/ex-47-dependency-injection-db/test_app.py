"""Tests for Example 47: FastAPI Depends() Supplies the DB Connection."""

import sqlite3

from fastapi.testclient import TestClient

import repository
from app import app

client = TestClient(app)


def test_list_tasks_via_injected_connection() -> None:
    response = client.get("/tasks")  # => exercises the full Depends() wiring end-to-end
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_connection_yields_and_then_closes() -> None:
    # => co-23: drive the DEPENDENCY generator directly, the way FastAPI does internally
    generator = repository.get_connection()
    connection = next(generator)  # => runs the code BEFORE "yield" -- connection is open
    assert isinstance(connection, sqlite3.Connection)
    connection.execute("SELECT 1")  # => still usable while the generator is suspended

    try:
        next(generator)  # => resumes AFTER "yield": runs finally, then raises StopIteration
    except StopIteration:
        pass  # => expected -- a generator dependency has exactly one yield point

    closed_after_cleanup = False
    try:
        connection.execute("SELECT 1")  # => the finally block already closed it
    except sqlite3.ProgrammingError:
        closed_after_cleanup = True
    assert closed_after_cleanup  # => co-23: cleanup genuinely ran, not just in theory
