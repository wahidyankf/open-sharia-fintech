"""Example 66: pytest verification for Flush Clearing Pending Tracking."""

import contextlib
import sqlite3

from example import UnitOfWork, User


def test_new_objects_is_empty_after_a_successful_flush() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.commit()  # => makes the schema visible
        uow = UnitOfWork(conn)
        uow.register_new(User(id=None, name="Grace"))
        uow.flush()
        assert uow.new_objects == []  # => cleared after flush


def test_second_flush_with_nothing_pending_writes_nothing() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        uow = UnitOfWork(conn)
        uow.register_new(User(id=None, name="Bob"))
        uow.flush()  # => first flush writes one row
        uow.flush()  # => second flush -- nothing pending
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 1  # => no duplicate write


# => Run: pytest -- Output: 2 passed
