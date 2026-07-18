"""Example 62: Flush Ordering -- a Parent's INSERT Runs Before Its Child's."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the two related domain objects being flushed
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => the PARENT object -- must exist before any child can reference it
class Customer:  # => the parent row's owning table
    id: int | None  # => None until flush() assigns it -- the ORDER's FK depends on this becoming real
    name: str  # => an ordinary column


@dataclasses.dataclass  # => the CHILD object -- holds a reference to the PARENT OBJECT, not a raw int
class Order:  # => references Customer via an object reference, resolved to a real id at flush time
    id: int | None  # => None until flush() assigns it
    customer: Customer  # => co-19: the FK value is READ from here, only after the parent is flushed
    total: float  # => an ordinary column


class UnitOfWork:  # => co-19 + co-20: orders new objects so parents flush before their children
    def __init__(self, conn: sqlite3.Connection) -> None:  # => needs a connection to flush against
        self._conn = conn  # => the ONE connection every flushed write goes through
        self._new_customers: list[Customer] = []  # => co-19: parents, flushed FIRST
        self._new_orders: list[Order] = []  # => co-19: children, flushed AFTER their parents

    def register_new_customer(self, customer: Customer) -> None:  # => tracks a parent
        self._new_customers.append(customer)  # => appended to the parent queue

    def register_new_order(self, order: Order) -> None:  # => tracks a child
        self._new_orders.append(order)  # => appended to the child queue -- NOT yet written

    def flush(self) -> None:  # => co-19: parents BEFORE children, unconditionally
        for customer in self._new_customers:  # => step 1: every parent's INSERT runs FIRST
            cursor = self._conn.execute("INSERT INTO customers(name) VALUES (?)", (customer.name,))  # => real write
            customer.id = cursor.lastrowid  # => assigns the real pk this order's FK will read below
        for order in self._new_orders:  # => step 2: children run ONLY after all parents are inserted
            assert order.customer.id is not None  # => co-19: the parent's pk MUST be real by this point
            cursor = self._conn.execute(  # => reads customer.id NOW -- guaranteed set by step 1 above
                "INSERT INTO orders(customer_id, total) VALUES (?, ?)",  # => the two placeholders below
                (order.customer.id, order.total),  # => order.customer.id is a REAL pk by this point
            )  # => would violate the FK if this ran before step 1 assigned customer.id
            order.id = cursor.lastrowid  # => assigns the order's own real pk too
        self._conn.commit()  # => makes both the parent and child rows durable together


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("PRAGMA foreign_keys = ON")  # => makes SQLite actually ENFORCE the FK below
    conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")  # => parent table
    conn.execute(  # => child table, FK REFERENCES customers -- SQLite rejects an orphan customer_id
        "CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), total REAL)"  # => the DDL
    )  # => enforced because PRAGMA foreign_keys is ON above
    conn.commit()  # => makes the schema visible
    uow = UnitOfWork(conn)  # => co-19 + co-20: one unit of work over this connection
    alice = Customer(id=None, name="Alice")  # => the parent, not yet persisted -- id is None right now
    order = Order(id=None, customer=alice, total=10.0)  # => co-19: references the OBJECT, not alice.id
    uow.register_new_customer(alice)  # => tracked as a new parent
    uow.register_new_order(order)  # => tracked as a new child
    uow.flush()  # => co-19: customers loop runs first, assigning alice.id BEFORE the orders loop reads it
    row = conn.execute("SELECT customer_id FROM orders WHERE id = ?", (order.id,)).fetchone()  # => the real FK
    assert row is not None and row[0] == alice.id  # => the child's stored FK matches the parent's real pk
    print(row[0] == alice.id)  # => Output: True
