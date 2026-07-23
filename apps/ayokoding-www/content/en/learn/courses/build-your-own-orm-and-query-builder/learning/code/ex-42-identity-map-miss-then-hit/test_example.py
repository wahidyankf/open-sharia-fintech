"""Example 42: pytest verification for Identity Map Miss-Then-Hit."""

import contextlib
import sqlite3

from example import IdentityMap


def test_first_load_counts_as_one_query() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.execute("INSERT INTO users VALUES (7, 'Grace')")  # => one seed row
        conn.commit()  # => makes the seed row visible
        identity_map = IdentityMap()
        identity_map.load(conn, 7)  # => a miss -- issues one query
        assert identity_map.query_count == 1  # => exactly one


def test_repeated_loads_never_add_further_queries() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'A')")
        conn.commit()
        identity_map = IdentityMap()
        for _ in range(5):  # => load the SAME pk five times in a row
            identity_map.load(conn, 1)  # => only the FIRST of these is a miss
        assert identity_map.query_count == 1  # => four hits added zero additional queries


# => Run: pytest -- Output: 2 passed
