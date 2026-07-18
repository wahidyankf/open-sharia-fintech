"""Example 71: Fixing N+1 by Batch-Loading All Children in One Extra Query."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the two related domain objects this example loads
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => the parent object, mapped from one row each
class Customer:  # => the type this example lists, with orders attached WITHOUT per-item queries
    id: int  # => primary key
    name: str  # => an ordinary column


query_log: list[str] = []  # => co-22: records EVERY query this fixed version issues, in order


def list_customers_with_orders(conn: sqlite3.Connection) -> dict[int, list[tuple[int, float]]]:  # => the fix
    query_log.append("SELECT * FROM customers")  # => co-22: logs query 1
    customer_rows = conn.execute("SELECT id, name FROM customers").fetchall()  # => query 1: the parent list
    customer_ids = [row[0] for row in customer_rows]  # => co-22: EVERY customer's pk, gathered up front
    placeholders = ",".join("?" for _ in customer_ids)  # => co-22: one "?" per id -- an IN clause, not a loop
    query_log.append("SELECT * FROM orders WHERE customer_id IN (...)")  # => co-22: logs query 2, the ONLY child query
    order_rows = conn.execute(  # => co-22: ONE query fetches every child row for EVERY customer at once
        f"SELECT customer_id, id, total FROM orders WHERE customer_id IN ({placeholders})",  # => dynamic IN
        customer_ids,  # => bound safely, one value per "?" -- still co-02, never string-interpolated data
    ).fetchall()  # => the ENTIRE child dataset, in a single round trip
    by_customer: dict[int, list[tuple[int, float]]] = {cid: [] for cid in customer_ids}  # => co-14: pre-seeded buckets
    for customer_id, order_id, total in order_rows:  # => co-22: groups the ONE result set in memory, no extra queries
        by_customer[customer_id].append((order_id, total))  # => appended to the correct customer's bucket
    return by_customer  # => co-14: a complete, in-memory identity-mapped-by-key grouping of every child row


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")  # => parent table
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")  # => child table
    conn.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "Alice"), (2, "Bob"), (3, "Carol")])  # => 3 rows
    conn.executemany(  # => a few orders, spread across the three customers
        "INSERT INTO orders(customer_id, total) VALUES (?, ?)",  # => two placeholders per row
        [(1, 10.0), (2, 20.0), (3, 30.0)],  # => 3 rows
    )  # => one order per customer, for this example's purposes
    conn.commit()  # => makes every seed row visible
    grouped = list_customers_with_orders(conn)  # => co-22: the entire read completes in TWO queries, not N+1
    assert len(query_log) == 2  # => co-22: exactly 2 queries, regardless of how many customers exist
    assert grouped[1] == [(1, 10.0)]  # => co-14: customer 1's orders, correctly grouped from the batch result
    print(len(query_log))  # => Output: 2
