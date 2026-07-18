"""Example 46: pytest verification for Session-Owns-Connection."""

import contextlib
import sqlite3

from example import Session


def test_every_query_uses_the_same_connection_object() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        session = Session(conn)  # => wraps this one connection
        session.execute("CREATE TABLE t(x INTEGER)")  # => first query
        seen_first = session.connection  # => observed after the first query
        session.execute("INSERT INTO t VALUES (1)")  # => second query
        seen_second = session.connection  # => observed after the second query
        assert seen_first is seen_second is conn  # => identical object across every call


def test_session_never_opens_a_second_connection() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        session = Session(conn)
        for _ in range(5):  # => five separate queries through the same session
            session.execute("SELECT 1")
        assert session.connection is conn  # => still the ONE connection handed in at construction


# => Run: pytest -- Output: 2 passed
