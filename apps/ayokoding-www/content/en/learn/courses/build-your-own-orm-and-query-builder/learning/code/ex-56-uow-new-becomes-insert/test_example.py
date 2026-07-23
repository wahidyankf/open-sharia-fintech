"""Example 56: pytest verification for New-Set Flush Becoming Real INSERTs."""

import contextlib
import sqlite3

from example import UnitOfWork, User


def test_flush_assigns_a_real_primary_key() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.commit()  # => makes the schema visible
        uow = UnitOfWork(conn)
        user = User(id=None, name="Grace")  # => no pk yet
        uow.register_new(user)
        uow.flush()  # => issues the real INSERT
        assert user.id is not None  # => pk assigned after flush


def test_flushed_new_set_becomes_empty() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        uow = UnitOfWork(conn)
        uow.register_new(User(id=None, name="A"))  # => two objects registered
        uow.register_new(User(id=None, name="B"))
        uow.flush()
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 2  # => both became real rows


# => Run: pytest -- Output: 2 passed
