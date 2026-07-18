"""Example 71: pytest verification for N+1 Fixed via Batch Loading."""

import contextlib
import sqlite3

import example
from example import list_customers_with_orders


def test_query_count_stays_at_two_regardless_of_customer_count() -> None:
    example.query_log = []  # => resets the module-level log for this test's own count
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")  # => parent table
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")  # => child
        conn.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "A"), (2, "B"), (3, "C"), (4, "D")])  # => 4 rows
        conn.commit()  # => makes every seed row visible
        list_customers_with_orders(conn)  # => two queries total, no matter how many customers
        assert len(example.query_log) == 2  # => 1 (parents) + 1 (batched children), never N+1


def test_grouping_correctly_buckets_each_customers_own_orders() -> None:
    example.query_log = []  # => resets the log again for isolation
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")
        conn.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "A"), (2, "B")])
        conn.executemany("INSERT INTO orders(customer_id, total) VALUES (?, ?)", [(1, 1.0), (1, 2.0), (2, 3.0)])
        conn.commit()
        grouped = list_customers_with_orders(conn)
        assert len(grouped[1]) == 2  # => customer 1's two orders, correctly grouped
        assert len(grouped[2]) == 1  # => customer 2's one order, correctly grouped


# => Run: pytest -- Output: 2 passed
