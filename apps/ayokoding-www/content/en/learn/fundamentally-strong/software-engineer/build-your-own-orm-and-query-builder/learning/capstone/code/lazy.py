# pyright: strict
"""Capstone: lazy.py -- a descriptor-based lazy relationship (co-21), attached ON TOP of
domain.py's plain Customer without changing that class at all, demonstrating both the N+1
it can cause (co-22) and the eager batch-load fix that collapses it to exactly 2 queries --
built on query_builder.py (co-01..co-08), the same builder every other step in this capstone
uses, not a hand-written SQL string.
"""

import sqlite3

import query_builder
from domain import Customer, Order
from mapper import load_order

QUERY_LOG: list[str] = []  # => co-22: records EVERY query this module issues, in the order it ran


class LazyOrders:  # => co-21: caches per-instance via __set_name__, the loader receives the owning instance
    def __init__(self) -> None:
        self._private_name = ""  # => placeholder, OVERWRITTEN by __set_name__ before any real use

    def __set_name__(self, owner: type, name: str) -> None:  # => called ONCE, at class body execution
        self._private_name = f"_lazy_{name}"  # => "orders" becomes "_lazy_orders" -- unique per attribute

    def __get__(self, instance: "CustomerWithOrders", owner: type) -> list[Order]:  # => called on every read
        if not hasattr(instance, self._private_name):  # => co-21: THIS instance has never loaded it before
            setattr(instance, self._private_name, _load_orders_for(instance))  # => stores the result ON the instance
        return getattr(instance, self._private_name)  # => co-21: a per-instance cache, not shared across instances


def _load_orders_for(customer: "CustomerWithOrders") -> list[Order]:  # => co-21's actual loader, co-01..co-08 built
    sql, params = query_builder.select("customer_order").where("customer_id", customer.id).compile()
    QUERY_LOG.append(sql)  # => co-22: logged so the scenario below can COUNT queries, not just eyeball code
    rows = customer.conn.execute(sql, params).fetchall()  # => the real query, scoped to THIS customer only
    return [load_order(row) for row in rows]  # => co-10: mapped into typed Order objects


class CustomerWithOrders(Customer):  # => adds the lazy relationship WITHOUT touching domain.Customer's fields
    orders = LazyOrders()  # => co-21: wired ONCE at the class level, shared by every instance

    def __init__(self, conn: sqlite3.Connection, id: int, name: str, email: str) -> None:
        super().__init__(id=id, name=name, email=email)  # => the plain Customer fields, untouched
        self.conn = conn  # => THIS instance's own connection -- what its lazy query will run against


def load_all_customers_naive(conn: sqlite3.Connection) -> list[CustomerWithOrders]:  # => query 1 only, per call
    sql, params = query_builder.select("customer").compile()
    QUERY_LOG.append(sql)
    rows = conn.execute(sql, params).fetchall()
    return [CustomerWithOrders(conn, id=row[0], name=row[1], email=row[2]) for row in rows]  # => co-10, mapped


def load_all_customers_with_orders_eager(conn: sqlite3.Connection) -> dict[int, list[Order]]:  # => co-22: THE fix
    sql, params = query_builder.select("customer").compile()  # => query 1: every parent, in one round trip
    QUERY_LOG.append(sql)
    customer_rows = conn.execute(sql, params).fetchall()
    ids = [row[0] for row in customer_rows]  # => co-22: every customer's pk, gathered up front for the batch below
    placeholders = ",".join("?" for _ in ids)  # => co-02: one "?" per id -- an IN clause, never a per-item loop
    order_sql = f"SELECT id, customer_id, item, amount, placed_on FROM customer_order WHERE customer_id IN ({placeholders})"  # => co-22: query 2 -- the ONLY child query, regardless of how many customers exist
    QUERY_LOG.append(order_sql)
    order_rows = conn.execute(order_sql, ids).fetchall()  # => the ENTIRE child dataset, in a single round trip
    grouped: dict[int, list[Order]] = {cid: [] for cid in ids}  # => co-22: pre-seeded per-customer buckets
    for row in order_rows:
        order = load_order(row)  # => co-10: mapped into a typed Order, exactly like the naive path
        grouped[order.customer_id].append(order)  # => appended to the correct customer's bucket
    return grouped  # => every customer's orders, fetched in exactly TWO queries total


if __name__ == "__main__":  # => guards against running the demo on `import lazy`
    import contextlib

    import migrations

    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        migrations.migrate(conn)
        conn.executemany(
            "INSERT INTO customer(name, email) VALUES (?, ?)",
            [("Ada", "ada@example.com"), ("Bob", "bob@example.com")],
        )
        conn.executemany(
            "INSERT INTO customer_order(customer_id, item, amount, placed_on) VALUES (?, ?, ?, ?)",
            [(1, "Keyboard", 79.5, "2026-07-18"), (1, "Mouse", 25.0, "2026-07-18"), (2, "Monitor", 199.0, "2026-07-18")],
        )
        conn.commit()

        QUERY_LOG.clear()  # => Phase 1 (co-21): per-instance caching -- a SECOND access must add NO query
        customers = load_all_customers_naive(conn)  # => query 1: the parent list
        first_access = customers[0].orders  # => co-21: FIRST access -- triggers the real query -- query 2
        second_access = customers[0].orders  # => co-21: SECOND access, SAME instance -- a cache hit, no new query
        print(len(QUERY_LOG))  # => Output: 2
        assert first_access is second_access  # => co-21: same cached list object, the second access added nothing
        assert len(QUERY_LOG) == 2  # => exactly query 1 (list) + query 2 (Ada's orders) -- Bob never touched here

        QUERY_LOG.clear()  # => Phase 2 (co-22): a NAIVE loop over every customer -- this is the N+1 pattern
        customers = load_all_customers_naive(conn)  # => query 1: the parent list, again
        for customer in customers:  # => co-22: one SEPARATE query PER customer -- the source of the N+1
            customer.orders  # => a fresh instance each time load_all_customers_naive() runs -- no cache carries over
        print(len(QUERY_LOG))  # => Output: 3
        assert len(QUERY_LOG) == 1 + len(customers)  # => co-22: 1 (list) + 2 (one per customer) = 3, observably

        QUERY_LOG.clear()  # => Phase 3 (co-22): the FIX -- batch-load every customer's orders in one extra query
        grouped = load_all_customers_with_orders_eager(conn)  # => co-22: collapses to exactly 2 queries, always
        print(len(QUERY_LOG))  # => Output: 2
        assert len(QUERY_LOG) == 2  # => co-22: exactly 2, regardless of how many customers existed
        assert len(grouped[1]) == 2 and len(grouped[2]) == 1  # => co-14: correctly grouped, per customer
