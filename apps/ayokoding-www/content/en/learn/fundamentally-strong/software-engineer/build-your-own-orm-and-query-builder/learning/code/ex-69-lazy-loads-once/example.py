"""Example 69: A Lazy Relationship Attribute Issues Its Query Exactly Once Per Instance."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any, Callable  # => the loader now takes the OWNING instance as its argument


class LazyAttribute:  # => co-21: caches per-instance, loader receives the instance to query with
    def __init__(self, loader: Callable[[Any], Any]) -> None:  # => `loader(instance)` -- needs the owner
        self._loader = loader  # => the deferred, instance-aware query, stored but not yet run
        self._private_name = ""  # => placeholder, overwritten by __set_name__

    def __set_name__(self, owner: type, name: str) -> None:  # => scopes the cache slot per attribute name
        self._private_name = f"_lazy_{name}"  # => e.g. "orders" becomes "_lazy_orders"

    def __get__(self, instance: object, owner: type) -> Any:  # => called on every attribute read
        if not hasattr(instance, self._private_name):  # => this instance has never queried yet
            setattr(instance, self._private_name, self._loader(instance))  # => runs the REAL query, scoped to instance
        return getattr(instance, self._private_name)  # => the cached, already-queried result


query_count = 0  # => co-21 + co-13: instrumented so this example can PROVE "exactly once per instance"


def load_orders_for(customer: "Customer") -> list[tuple[int, float]]:  # => co-21's actual loader function
    global query_count  # => mutates the module-level counter
    query_count += 1  # => co-21: counts EVERY time this actually runs
    rows = customer.conn.execute(  # => co-13: scoped by THIS customer's own customer_id
        "SELECT id, total FROM orders WHERE customer_id = ?",  # => one placeholder, bound below
        (customer.customer_id,),  # => a single-element params tuple -- co-02's placeholder rule
    ).fetchall()  # => a real list of (id, total) tuples for THIS customer only
    return rows  # => the query result, about to be cached by the descriptor above


class Customer:  # => a domain object whose "orders" attribute is a lazy, query-backed relationship
    orders = LazyAttribute(load_orders_for)  # => co-21: wired ONCE at the class level, shared by every instance

    def __init__(self, conn: sqlite3.Connection, customer_id: int) -> None:  # => needs the connection + own pk
        self.conn = conn  # => the connection this instance's lazy query will run against
        self.customer_id = customer_id  # => this instance's own primary key -- scopes the query above


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")  # => real table
    conn.executemany("INSERT INTO orders(customer_id, total) VALUES (?, ?)", [(1, 10.0), (1, 20.0)])  # => two rows
    conn.commit()  # => makes both seed rows visible
    customer = Customer(conn, customer_id=1)  # => construction alone must NOT trigger a query
    assert query_count == 0  # => confirmed -- no query has run yet
    first_access = customer.orders  # => co-21: FIRST access -- THIS triggers the real query
    assert query_count == 1  # => exactly one query so far
    second_access = customer.orders  # => co-21: SECOND access -- must be a cache hit, no new query
    assert query_count == 1  # => co-21: still exactly one -- the second access added nothing
    assert first_access is second_access  # => the SAME cached list object, not a re-queried copy
    print(query_count)  # => Output: 1
