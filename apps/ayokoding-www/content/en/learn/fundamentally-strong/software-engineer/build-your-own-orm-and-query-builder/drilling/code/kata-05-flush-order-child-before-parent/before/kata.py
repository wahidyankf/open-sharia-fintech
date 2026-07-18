# pyright: strict
"""Kata 5 (before): flushing orders BEFORE their parent customer is inserted means the
FK column is still the -1 placeholder when the INSERT runs, violating the FK constraint
the database itself enforces -- a real, observable IntegrityError, not a silent wrong value (co-19)."""

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
    customer_id: int  # -1 until the parent's real id is known
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
        # BUG: orders are inserted FIRST -- customer.id is still None, so order.customer_id
        # stays at its -1 placeholder instead of ever being resolved to a real value.
        for order, customer in self._new_orders:
            order.customer_id = customer.id if customer.id is not None else -1
            cur = self._conn.execute("INSERT INTO orders(customer_id, item) VALUES (?, ?)", (order.customer_id, order.item))
            order.id = cur.lastrowid
        for customer in self._new_customers:
            cur = self._conn.execute("INSERT INTO customers(name) VALUES (?)", (customer.name,))
            customer.id = cur.lastrowid
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
    try:
        uow.flush()
    except sqlite3.IntegrityError as exc:
        print(f"IntegrityError: {exc}")
