"""Example 70: Naive Lazy Loading Over a List Produces N+1 Queries, Observably."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the two related domain objects this example loads
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => the parent object, mapped from one row each
class Customer:  # => the type this example lists, then lazily loads orders FOR each one
    id: int  # => primary key
    name: str  # => an ordinary column


query_log: list[str] = []  # => co-22: records EVERY query this example issues, in order


def list_customers(conn: sqlite3.Connection) -> list[Customer]:  # => query 1: the initial list
    query_log.append("SELECT * FROM customers")  # => co-22: logs the query about to run
    rows = conn.execute("SELECT id, name FROM customers").fetchall()  # => the ONE query for the whole list
    return [Customer(id=row[0], name=row[1]) for row in rows]  # => co-10: mapped into typed objects


def orders_for(conn: sqlite3.Connection, customer_id: int) -> list[tuple[int, float]]:  # => query 2..N+1
    query_log.append(f"SELECT * FROM orders WHERE customer_id = {customer_id}")  # => co-22: logs EACH separate query
    return conn.execute(  # => co-22: this runs ONCE PER customer -- the N+1 pattern this example makes visible
        "SELECT id, total FROM orders WHERE customer_id = ?",  # => this customer's own child query
        (customer_id,),  # => one bound placeholder
    ).fetchall()  # => this customer's own orders, fetched independently


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")  # => parent table
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")  # => child table
    conn.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "Alice"), (2, "Bob"), (3, "Carol")])  # => 3 rows
    conn.executemany(  # => a few orders, spread across the three customers
        "INSERT INTO orders(customer_id, total) VALUES (?, ?)",  # => two placeholders per row
        [(1, 10.0), (2, 20.0), (3, 30.0)],  # => 3 rows
    )  # => one order per customer, for this example's purposes
    conn.commit()  # => makes every seed row visible
    customers = list_customers(conn)  # => co-22: query 1 -- the ONE list query
    for customer in customers:  # => co-22: naive per-item loop -- the source of the N+1 pattern
        orders_for(conn, customer.id)  # => co-22: ONE separate query PER customer -- N additional queries
    assert len(query_log) == 1 + len(customers)  # => co-22: exactly 1 (list) + N (per-item) queries, observably
    print(len(query_log))  # => Output: 4
