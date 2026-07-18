"""Example 64: pytest verification for Flush Atomic Commit."""

import contextlib
import sqlite3

from example import UnitOfWork, User


def test_all_pending_writes_land_after_one_flush() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.commit()  # => makes the schema visible
        uow = UnitOfWork(conn)
        for name in ("A", "B", "C", "D"):  # => four pending objects
            uow.register_new(User(id=None, name=name))
        uow.flush()  # => one atomic flush
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 4  # => all four landed together


def test_every_flushed_object_gets_a_distinct_pk() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        uow = UnitOfWork(conn)
        a = User(id=None, name="A")  # => two objects
        b = User(id=None, name="B")
        uow.register_new(a)
        uow.register_new(b)
        uow.flush()
        assert a.id != b.id  # => distinct pks, both real


# => Run: pytest -- Output: 2 passed
