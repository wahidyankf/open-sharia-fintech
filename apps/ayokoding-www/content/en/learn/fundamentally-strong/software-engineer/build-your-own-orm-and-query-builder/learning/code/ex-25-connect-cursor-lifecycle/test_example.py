"""Example 25: pytest verification for the Full PEP 249 Lifecycle."""

import contextlib
import sqlite3


def test_every_pep_249_stage_runs_in_order() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => connect()
        conn.execute("CREATE TABLE t(id INTEGER PRIMARY KEY)")  # => schema setup
        conn.execute("INSERT INTO t(id) VALUES (1), (2), (3)")  # => three seed rows
        conn.commit()  # => makes the seed rows durable/visible
        cur = conn.cursor()  # => cursor()
        cur.execute("SELECT id FROM t ORDER BY id")  # => execute()
        rows = cur.fetchall()  # => fetchall()
        cur.close()  # => explicit cursor close
        assert rows == [(1,), (2,), (3,)]  # => all three rows came back, in order
        assert cur.connection is conn  # => the closed cursor still remembers its own connection


# => Run: pytest -- Output: 1 passed
