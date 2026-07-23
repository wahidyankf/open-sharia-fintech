"""Example 70: pytest verification for the Observable N+1 Query Pattern."""

import contextlib
import sqlite3

import example
from example import list_customers, orders_for


def test_query_count_equals_one_plus_customer_count() -> None:
    example.query_log = []  # => resets the module-level log for this test's own count
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")  # => parent table
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")  # => child
        conn.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "A"), (2, "B")])  # => two customers
        conn.commit()  # => makes both seed rows visible
        customers = list_customers(conn)  # => query 1
        for customer in customers:  # => N additional queries, one per customer
            orders_for(conn, customer.id)
        assert len(example.query_log) == 1 + 2  # => 1 list query + 2 per-customer queries = 3


def test_zero_customers_means_exactly_one_query() -> None:
    example.query_log = []  # => resets the log again for isolation
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")
        conn.commit()
        list_customers(conn)  # => the ONE list query, no per-item loop needed since there are no rows
        assert len(example.query_log) == 1  # => just the initial list query, no N+1 at all


# => Run: pytest -- Output: 2 passed
