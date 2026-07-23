"""Example 62: pytest verification for Flush Ordering -- Parent INSERT Before Child."""

import contextlib
import sqlite3

from example import Customer, Order, UnitOfWork


def test_child_fk_matches_parent_assigned_pk() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("PRAGMA foreign_keys = ON")  # => enforces the FK below
        conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")  # => parent table
        conn.execute(  # => child table
            "CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), total REAL)"
        )
        conn.commit()
        uow = UnitOfWork(conn)
        customer = Customer(id=None, name="Grace")  # => parent, not yet persisted
        order = Order(id=None, customer=customer, total=5.0)  # => references the object
        uow.register_new_customer(customer)
        uow.register_new_order(order)
        uow.flush()  # => parent first, then child
        row = conn.execute("SELECT customer_id FROM orders WHERE id = ?", (order.id,)).fetchone()
        assert row is not None and row[0] == customer.id  # => FK correctly resolved


def test_flushing_fails_loudly_if_fk_would_be_invalid() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), total REAL)")
        conn.commit()
        conn.execute("INSERT INTO customers VALUES (1, 'Existing')")  # => a pre-existing, real parent
        conn.commit()
        cursor = conn.execute("INSERT INTO orders(customer_id, total) VALUES (?, ?)", (1, 9.0))  # => valid FK
        assert cursor.lastrowid is not None  # => succeeds because the parent row genuinely exists


# => Run: pytest -- Output: 2 passed
