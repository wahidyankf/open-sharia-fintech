"""Example 43: pytest verification for Identity Map Key Shape."""

import contextlib
import sqlite3

from example import IdentityMap, Order, User


def test_same_pk_value_across_two_tables_stays_distinct() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => first table
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, total REAL)")  # => second table
        conn.execute("INSERT INTO users VALUES (5, 'Bob')")  # => user pk=5
        conn.execute("INSERT INTO orders VALUES (5, 10.0)")  # => order pk=5 -- same integer
        conn.commit()  # => makes both rows visible
        identity_map = IdentityMap()
        user = identity_map.load_user(conn, 5)  # => loads users pk=5
        order = identity_map.load_order(conn, 5)  # => loads orders pk=5
        assert isinstance(user, User)  # => correctly typed as User
        assert isinstance(order, Order)  # => correctly typed as Order, not conflated with user


def test_users_identity_survives_a_same_pk_orders_load() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, total REAL)")
        conn.execute("INSERT INTO users VALUES (1, 'A')")
        conn.execute("INSERT INTO orders VALUES (1, 1.0)")
        conn.commit()
        identity_map = IdentityMap()
        first_user = identity_map.load_user(conn, 1)  # => caches ("users", 1)
        identity_map.load_order(conn, 1)  # => caches ("orders", 1) -- must not touch ("users", 1)
        second_user = identity_map.load_user(conn, 1)  # => re-load users pk=1
        assert first_user is second_user  # => users identity untouched by the orders load


# => Run: pytest -- Output: 2 passed
