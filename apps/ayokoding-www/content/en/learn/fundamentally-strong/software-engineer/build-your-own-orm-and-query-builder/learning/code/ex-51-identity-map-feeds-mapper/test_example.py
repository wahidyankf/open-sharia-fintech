"""Example 51: pytest verification for Identity-Map-Feeds-Mapper."""

import contextlib
import sqlite3

from example import IdentityMap, Mapper


def test_second_load_of_same_pk_does_not_call_the_mapper() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.execute("INSERT INTO users VALUES (9, 'Grace')")  # => one seed row
        conn.commit()  # => makes the seed row visible
        mapper = Mapper()
        identity_map = IdentityMap(mapper)
        identity_map.load(conn, 9)  # => first load, a miss
        identity_map.load(conn, 9)  # => second load, a hit
        assert mapper.construct_count == 1  # => the mapper ran exactly once


def test_different_pks_each_trigger_one_construction() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'A'), (2, 'B')")
        conn.commit()
        mapper = Mapper()
        identity_map = IdentityMap(mapper)
        identity_map.load(conn, 1)  # => miss for pk 1
        identity_map.load(conn, 2)  # => miss for pk 2 -- a DIFFERENT key
        assert mapper.construct_count == 2  # => two distinct pks, two constructions


# => Run: pytest -- Output: 2 passed
