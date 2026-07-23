"""Example 75: pytest verification for the Full Wired Read Stack."""

import contextlib
import sqlite3

from example import IdentityMap, Select


def test_two_queries_over_the_same_row_return_the_identical_object() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.executemany("INSERT INTO users VALUES (?, ?)", [(1, "A"), (2, "B")])  # => two rows
        conn.commit()  # => makes both rows visible
        stack = IdentityMap(conn)
        first = stack.select(Select(table="users"))  # => all rows
        second = stack.select(Select(table="users").where_id_gt(0))  # => also all rows, different query
        assert first[0] is second[0]  # => same pk, same object, across two DIFFERENT compiled queries


def test_where_filter_narrows_the_mapped_result_set() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.executemany("INSERT INTO users VALUES (?, ?)", [(1, "A"), (2, "B"), (3, "C")])
        conn.commit()
        stack = IdentityMap(conn)
        results = stack.select(Select(table="users").where_id_gt(1))  # => only ids 2 and 3
        assert [u.id for u in results] == [2, 3]  # => filtered, mapped, and identity-mapped correctly


# => Run: pytest -- Output: 2 passed
