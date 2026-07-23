# pyright: strict
"""Kata 6 (after): one batched IN (...) query fetches every customer's orders together --
exactly 2 queries total, regardless of how many customers exist (co-21, co-22)."""

import contextlib
import sqlite3

QUERY_LOG: list[str] = []


def load_all_with_orders(conn: sqlite3.Connection) -> dict[int, list[tuple[int, str]]]:
    QUERY_LOG.append("SELECT * FROM customers")
    customer_rows = conn.execute("SELECT id, name FROM customers").fetchall()
    ids = [row[0] for row in customer_rows]
    placeholders = ",".join("?" for _ in ids)  # THE FIX: ONE batched query, not one per customer
    QUERY_LOG.append("SELECT * FROM orders WHERE customer_id IN (...)")
    order_rows = conn.execute(f"SELECT customer_id, id, item FROM orders WHERE customer_id IN ({placeholders})", ids).fetchall()
    grouped: dict[int, list[tuple[int, str]]] = {cid: [] for cid in ids}
    for customer_id, order_id, item in order_rows:
        grouped[customer_id].append((order_id, item))
    return grouped


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, item TEXT)")
    conn.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "Ada"), (2, "Bob"), (3, "Carol")])
    conn.executemany("INSERT INTO orders(customer_id, item) VALUES (?, ?)", [(1, "Keyboard"), (2, "Mouse"), (3, "Monitor")])
    conn.commit()

    QUERY_LOG.clear()
    grouped = load_all_with_orders(conn)
    print(len(QUERY_LOG))
