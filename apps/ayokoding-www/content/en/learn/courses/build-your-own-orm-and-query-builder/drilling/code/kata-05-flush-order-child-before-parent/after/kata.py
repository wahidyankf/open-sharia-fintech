# pyright: strict
"""Kata 5 (after): customers flush FIRST, so every order's FK is resolved to a REAL id
before its own INSERT ever runs -- the FK constraint is satisfied by construction (co-19)."""

import contextlib
import dataclasses
import sqlite3


@dataclasses.dataclass
class Customer:
    id: int | None
    name: str


@dataclasses.dataclass
class Order:
    id: int | None
    customer_id: int
    item: str


class UnitOfWork:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._new_customers: list[Customer] = []
        self._new_orders: list[tuple[Order, Customer]] = []

    def register_new_customer(self, customer: Customer) -> None:
        self._new_customers.append(customer)

    def register_new_order(self, order: Order, customer: Customer) -> None:
        self._new_orders.append((order, customer))

    def flush(self) -> None:
        # THE FIX: customers flush FIRST -- every order's parent has a real id before step 2 runs.
        for customer in self._new_customers:
            cur = self._conn.execute("INSERT INTO customers(name) VALUES (?)", (customer.name,))
            customer.id = cur.lastrowid
        for order, customer in self._new_orders:
            assert customer.id is not None  # guaranteed real -- the loop above already ran
            order.customer_id = customer.id
            cur = self._conn.execute("INSERT INTO orders(customer_id, item) VALUES (?, ?)", (order.customer_id, order.item))
            order.id = cur.lastrowid
        self._conn.commit()


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), item TEXT)")
    conn.commit()
    uow = UnitOfWork(conn)
    ada = Customer(id=None, name="Ada")
    order = Order(id=None, customer_id=-1, item="Keyboard")
    uow.register_new_customer(ada)
    uow.register_new_order(order, ada)
    uow.flush()
    stored = conn.execute("SELECT customer_id FROM orders WHERE id = ?", (order.id,)).fetchone()
    print(stored[0], ada.id, stored[0] == ada.id)
