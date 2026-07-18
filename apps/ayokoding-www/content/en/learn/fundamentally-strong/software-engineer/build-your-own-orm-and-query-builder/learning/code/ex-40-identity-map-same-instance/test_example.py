"""Example 40: pytest verification for Identity Map Same-Instance Guarantee."""

import contextlib
import sqlite3

from example import IdentityMap


def test_two_loads_of_same_pk_return_identical_instance() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.execute("INSERT INTO users VALUES (5, 'Grace')")  # => one seed row
        conn.commit()  # => makes the seed row visible
        identity_map = IdentityMap()  # => a fresh map for this test
        first = identity_map.load(conn, 5)  # => first load
        second = identity_map.load(conn, 5)  # => second load, same pk
        assert first is second  # => the core co-13 guarantee


def test_mutating_the_cached_instance_is_visible_on_next_load() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'Bob')")
        conn.commit()
        identity_map = IdentityMap()
        first = identity_map.load(conn, 1)  # => load once
        first.name = "Bobby"  # => mutate the cached instance in place
        second = identity_map.load(conn, 1)  # => load again -- must be the SAME mutated object
        assert second.name == "Bobby"  # => proves it's the same object, not a fresh reload


# => Run: pytest -- Output: 2 passed
