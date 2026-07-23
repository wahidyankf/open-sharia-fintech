"""Example 47: pytest verification for Session begin/write/commit."""

import contextlib
import sqlite3

from example import Session


def test_row_is_present_after_commit() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE items(id INTEGER PRIMARY KEY, label TEXT)")  # => schema
        conn.commit()  # => schema committed before the session's transaction starts
        session = Session(conn)
        session.execute("INSERT INTO items VALUES (1, 'widget')")  # => pending write
        session.commit()  # => makes it durable
        row = session.execute("SELECT label FROM items WHERE id = 1").fetchone()
        assert row is not None and row[0] == "widget"  # => present after commit


def test_multiple_writes_before_one_commit_all_persist() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE items(id INTEGER PRIMARY KEY)")
        conn.commit()
        session = Session(conn)
        session.execute("INSERT INTO items VALUES (1)")  # => two writes, one shared transaction
        session.execute("INSERT INTO items VALUES (2)")
        session.commit()  # => a SINGLE commit makes both durable
        count = session.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        assert count == 2  # => both rows survived


# => Run: pytest -- Output: 2 passed
