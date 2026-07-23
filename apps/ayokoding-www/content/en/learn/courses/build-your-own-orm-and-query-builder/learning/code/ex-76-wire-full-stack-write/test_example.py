"""Example 76: pytest verification for the Full Wired Write Stack."""

import contextlib
import sqlite3

from example import Session, User


def test_add_then_commit_persists_a_real_row() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.commit()  # => makes the schema visible
        session = Session(conn)
        user = User(id=None, name="Grace")  # => not yet persisted
        session.add(user)
        session.commit()  # => the full write path
        rows = session.query_all()
        assert rows == [(user.id, "Grace")]  # => durable, with the assigned pk


def test_multiple_added_objects_all_commit_together() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        session = Session(conn)
        session.add(User(id=None, name="A"))  # => two pending objects
        session.add(User(id=None, name="B"))
        session.commit()
        rows = session.query_all()
        assert len(rows) == 2  # => both landed together


# => Run: pytest -- Output: 2 passed
