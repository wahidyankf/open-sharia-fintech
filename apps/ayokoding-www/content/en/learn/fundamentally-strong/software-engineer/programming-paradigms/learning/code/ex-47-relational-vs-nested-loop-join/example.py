"""Example 47: Relational vs Nested-Loop Join."""

import sqlite3  # => the standard library's built-in SQL engine -- no external dependency needed

customers: list[tuple[int, str]] = [(1, "alice"), (2, "bob")]  # => (customer_id, name)
orders: list[tuple[int, int, str]] = [(101, 1, "widget"), (102, 2, "gadget"), (103, 1, "gizmo")]
# => (order_id, customer_id, item)


def join_via_sql(customers: list[tuple[int, str]], orders: list[tuple[int, int, str]]) -> list[tuple[str, str]]:  # => declarative leg
    conn = sqlite3.connect(":memory:")  # => declare tables, state the join, let SQLite compute it
    conn.execute("CREATE TABLE customers (id INTEGER, name TEXT)")  # => declares the shape, no data yet
    conn.execute("CREATE TABLE orders (id INTEGER, customer_id INTEGER, item TEXT)")  # => same, for orders
    conn.executemany("INSERT INTO customers VALUES (?, ?)", customers)  # => load every customer row
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?)", orders)  # => load every order row
    rows = conn.execute(  # => the query IS the join -- no accumulator variable anywhere in this function
        "SELECT customers.name, orders.item FROM customers JOIN orders ON customers.id = orders.customer_id ORDER BY orders.id"
        # => JOIN...ON declares the relationship -- no explicit loop nesting anywhere in this code
    ).fetchall()  # => the query planner decided HOW to match rows; this call only asks for the results
    conn.close()  # => release the in-memory connection
    return rows  # => list of (name, item) pairs


def join_via_nested_loop(customers: list[tuple[int, str]], orders: list[tuple[int, int, str]]) -> list[tuple[str, str]]:  # => imperative leg
    result: list[tuple[str, str]] = []  # => mutable accumulator
    for _order_id, customer_id, item in orders:  # => outer loop: every order, in insertion order
        for cid, name in customers:  # => inner loop: scan every customer looking for a match
            if cid == customer_id:  # => the join condition, written out explicitly as a comparison
                result.append((name, item))  # => explicit accumulation, one matched pair at a time
                break  # => stop scanning customers once this order's match is found
    return result  # => the fully built accumulator


sql_result = join_via_sql(customers, orders)  # => declarative version
loop_result = join_via_nested_loop(customers, orders)  # => imperative version

print(sql_result)  # => both must produce identical (name, item) pairs, in the same order
# => Output: [('alice', 'widget'), ('bob', 'gadget'), ('alice', 'gizmo')]
print(sql_result == loop_result)  # => confirms the declarative and imperative joins agree
# => Output: True
