"""Example 61: pytest verification for Deleted-Set Flush Becoming Real DELETEs."""

import contextlib
import sqlite3

from example import UnitOfWork, User


def test_flush_removes_the_row() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.execute("INSERT INTO users VALUES (1, 'Grace')")  # => one seed row
        conn.commit()  # => makes the seed row visible
        uow = UnitOfWork(conn)
        uow.register_deleted(User(id=1, name="Grace"))
        uow.flush()  # => issues the real DELETE
        row = conn.execute("SELECT * FROM users WHERE id = 1").fetchone()
        assert row is None  # => genuinely gone


def test_flushed_deleted_set_becomes_empty() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.executemany("INSERT INTO users VALUES (?, ?)", [(1, "A"), (2, "B")])  # => two rows
        conn.commit()
        uow = UnitOfWork(conn)
        uow.register_deleted(User(id=1, name="A"))  # => two objects registered
        uow.register_deleted(User(id=2, name="B"))
        uow.flush()
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 0  # => both rows removed


# => Run: pytest -- Output: 2 passed
