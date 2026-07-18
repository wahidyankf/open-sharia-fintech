"""Example 63: Flush Ordering -- a Child's DELETE Runs Before Its Parent's."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the two related domain objects being deleted
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => the PARENT object -- cannot be deleted while a child still references it
class Customer:  # => the parent row's owning table
    id: int  # => primary key -- a real, existing row
    name: str  # => an ordinary column


@dataclasses.dataclass  # => the CHILD object -- its FK row must be gone BEFORE the parent can go
class Order:  # => references Customer via customer_id
    id: int  # => primary key -- a real, existing row
    customer_id: int  # => co-19: must be deleted FIRST, or the parent's DELETE violates the FK


class UnitOfWork:  # => co-19 + co-20: orders deletions so children flush before their parents
    def __init__(self, conn: sqlite3.Connection) -> None:  # => needs a connection to flush against
        self._conn = conn  # => the ONE connection every flushed write goes through
        self._deleted_orders: list[Order] = []  # => co-19: children, deleted FIRST
        self._deleted_customers: list[Customer] = []  # => co-19: parents, deleted AFTER their children

    def register_deleted_order(self, order: Order) -> None:  # => tracks a child for removal
        self._deleted_orders.append(order)  # => appended to the child-deletion queue

    def register_deleted_customer(self, customer: Customer) -> None:  # => tracks a parent for removal
        self._deleted_customers.append(customer)  # => appended to the parent-deletion queue -- deleted LAST

    def flush(self) -> None:  # => co-19: children BEFORE parents, unconditionally, the REVERSE of insert order
        for order in self._deleted_orders:  # => step 1: every child's DELETE runs FIRST
            self._conn.execute("DELETE FROM orders WHERE id = ?", (order.id,))  # => removes the referencing row
        for customer in self._deleted_customers:  # => step 2: parents deleted ONLY after all children are gone
            self._conn.execute("DELETE FROM customers WHERE id = ?", (customer.id,))  # => now safe -- no referrers left
        self._conn.commit()  # => makes both deletions durable together


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("PRAGMA foreign_keys = ON")  # => makes SQLite actually ENFORCE the FK below
    conn.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT)")  # => parent table
    conn.execute(  # => child table, FK REFERENCES customers -- SQLite rejects deleting a referenced parent
        "CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id))"  # => the DDL
    )  # => enforced because PRAGMA foreign_keys is ON above
    conn.execute("INSERT INTO customers VALUES (1, 'Alice')")  # => the parent row
    conn.execute("INSERT INTO orders VALUES (1, 1)")  # => the child row, referencing customer id=1
    conn.commit()  # => makes both seed rows visible
    uow = UnitOfWork(conn)  # => co-19 + co-20: one unit of work over this connection
    uow.register_deleted_order(Order(id=1, customer_id=1))  # => tracked for removal FIRST
    uow.register_deleted_customer(Customer(id=1, name="Alice"))  # => tracked for removal SECOND
    uow.flush()  # => co-19: the order's DELETE runs before the customer's -- no FK violation
    remaining = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]  # => confirms the parent is gone too
    assert remaining == 0  # => both rows removed, in the SAFE order
    print(remaining)  # => Output: 0
