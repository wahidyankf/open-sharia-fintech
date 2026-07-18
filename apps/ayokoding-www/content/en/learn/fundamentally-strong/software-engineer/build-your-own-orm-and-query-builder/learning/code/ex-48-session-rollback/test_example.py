"""Example 48: pytest verification for Session begin/write/rollback."""

import contextlib
import sqlite3

from example import Session


def test_row_is_absent_after_rollback() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE items(id INTEGER PRIMARY KEY, label TEXT)")  # => schema
        conn.commit()  # => schema committed before the session's transaction starts
        session = Session(conn)
        session.execute("INSERT INTO items VALUES (1, 'widget')")  # => pending write
        session.rollback()  # => undoes it
        row = session.execute("SELECT * FROM items WHERE id = 1").fetchone()
        assert row is None  # => absent after rollback


def test_rollback_undoes_multiple_pending_writes_together() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE items(id INTEGER PRIMARY KEY)")
        conn.commit()
        session = Session(conn)
        session.execute("INSERT INTO items VALUES (1)")  # => two pending writes
        session.execute("INSERT INTO items VALUES (2)")
        session.rollback()  # => a SINGLE rollback undoes BOTH
        count = session.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        assert count == 0  # => neither row survived


# => Run: pytest -- Output: 2 passed
