# pyright: strict
"""Kata 6 (before): touching a lazy relationship inside a naive per-parent loop issues
one SEPARATE query per parent -- the N+1 pattern, reproduced and counted (co-21, co-22)."""

import contextlib
import dataclasses
import sqlite3

QUERY_LOG: list[str] = []


@dataclasses.dataclass
class Customer:
    id: int
    name: str
    conn: sqlite3.Connection

    @property
    def orders(self) -> list[tuple[int, str]]:
        # BUG: no caching AND called from inside a loop below -- one query PER customer.
        QUERY_LOG.append(f"SELECT * FROM orders WHERE customer_id = {self.id}")
        return self.conn.execute("SELECT id, item FROM orders WHERE customer_id = ?", (self.id,)).fetchall()


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, item TEXT)")
    conn.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "Ada"), (2, "Bob"), (3, "Carol")])
    conn.executemany("INSERT INTO orders(customer_id, item) VALUES (?, ?)", [(1, "Keyboard"), (2, "Mouse"), (3, "Monitor")])
    conn.commit()

    QUERY_LOG.clear()
    rows = conn.execute("SELECT id, name FROM customers").fetchall()
    QUERY_LOG.append("SELECT * FROM customers")
    customers = [Customer(id=r[0], name=r[1], conn=conn) for r in rows]
    for customer in customers:  # intent: just read each customer's orders -- looks harmless
        customer.orders
    print(len(QUERY_LOG))
