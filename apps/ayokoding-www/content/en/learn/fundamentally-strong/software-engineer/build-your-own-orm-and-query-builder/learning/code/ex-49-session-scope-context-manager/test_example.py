"""Example 49: pytest verification for Session as a Scoped Context Manager."""

import contextlib
import sqlite3

import pytest

from example import Session


def test_clean_exit_commits() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE t(id INTEGER PRIMARY KEY)")  # => schema
        conn.commit()
        with Session(conn) as session:
            session.execute("INSERT INTO t VALUES (1)")  # => pending, no exception in this block
        row = conn.execute("SELECT * FROM t WHERE id = 1").fetchone()
        assert row is not None  # => committed on clean exit


def test_exception_exit_rolls_back_and_still_propagates() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE t(id INTEGER PRIMARY KEY)")  # => schema
        conn.commit()
        with pytest.raises(RuntimeError):  # => confirms __exit__ returns False -- the error still propagates
            with Session(conn) as session:
                session.execute("INSERT INTO t VALUES (1)")  # => pending write
                raise RuntimeError("boom")  # => triggers the rollback branch
        row = conn.execute("SELECT * FROM t WHERE id = 1").fetchone()
        assert row is None  # => rolled back, not committed


# => Run: pytest -- Output: 2 passed
