"""Example 63: pytest verification for Flush Ordering -- Child DELETE Before Parent."""

import contextlib
import sqlite3

from example import Customer, Order, UnitOfWork


def test_child_and_parent_both_removed_without_fk_violation() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("PRAGMA foreign_keys = ON")  # => enforces the FK below
        conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")  # => parent table
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id))")
        conn.execute("INSERT INTO customers VALUES (1, 'Grace')")  # => parent row
        conn.execute("INSERT INTO orders VALUES (1, 1)")  # => child row, references parent
        conn.commit()
        uow = UnitOfWork(conn)
        uow.register_deleted_order(Order(id=1, customer_id=1))  # => child first
        uow.register_deleted_customer(Customer(id=1, name="Grace"))  # => parent second
        uow.flush()
        customers_left = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        orders_left = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        assert (customers_left, orders_left) == (0, 0)  # => both genuinely removed


def test_deleting_child_alone_leaves_parent_untouched() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id))")
        conn.execute("INSERT INTO customers VALUES (1, 'Bob')")
        conn.execute("INSERT INTO orders VALUES (1, 1)")
        conn.commit()
        uow = UnitOfWork(conn)
        uow.register_deleted_order(Order(id=1, customer_id=1))  # => only the child is registered
        uow.flush()
        customers_left = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        assert customers_left == 1  # => parent unaffected


# => Run: pytest -- Output: 2 passed
