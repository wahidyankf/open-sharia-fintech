"""Example 41: pytest verification for Identity Map Distinct-Keys Behavior."""

import contextlib
import sqlite3

from example import IdentityMap


def test_distinct_pks_produce_distinct_instances() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.execute("INSERT INTO users VALUES (10, 'Xu'), (20, 'Yara')")  # => two seed rows
        conn.commit()  # => makes both rows visible
        identity_map = IdentityMap()  # => a fresh map
        a = identity_map.load(conn, 10)  # => loads pk 10
        b = identity_map.load(conn, 20)  # => loads pk 20
        assert a is not b  # => distinct keys, distinct objects
        assert (a.id, b.id) == (10, 20)  # => each holds its own correct data


def test_each_pk_still_caches_independently() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'A'), (2, 'B')")
        conn.commit()
        identity_map = IdentityMap()
        first_load_of_1 = identity_map.load(conn, 1)  # => populates pk 1's cache slot
        identity_map.load(conn, 2)  # => populates pk 2's cache slot -- must not disturb pk 1's
        second_load_of_1 = identity_map.load(conn, 1)  # => re-load pk 1
        assert first_load_of_1 is second_load_of_1  # => pk 1's identity survived pk 2's load


# => Run: pytest -- Output: 2 passed
