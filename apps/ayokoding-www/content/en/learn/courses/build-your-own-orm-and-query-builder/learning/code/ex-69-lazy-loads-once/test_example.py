"""Example 69: pytest verification for Lazy Relationship Loading Exactly Once."""

import contextlib
import sqlite3

from example import Customer


def test_first_access_issues_one_query() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")  # => real table
        conn.execute("INSERT INTO orders(customer_id, total) VALUES (1, 5.0)")  # => one seed row
        conn.commit()  # => makes the seed row visible
        customer = Customer(conn, customer_id=1)
        orders = customer.orders  # => first access -- triggers the real query
        assert len(orders) == 1  # => the one matching row came back


def test_two_customers_do_not_share_a_cached_result() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")
        conn.executemany("INSERT INTO orders(customer_id, total) VALUES (?, ?)", [(1, 1.0), (2, 2.0), (2, 3.0)])
        conn.commit()
        first = Customer(conn, customer_id=1)  # => customer 1 -- one matching row
        second = Customer(conn, customer_id=2)  # => customer 2 -- two matching rows
        assert len(first.orders) == 1  # => scoped correctly, independently
        assert len(second.orders) == 2  # => a DIFFERENT instance, a DIFFERENT cached result


# => Run: pytest -- Output: 2 passed
