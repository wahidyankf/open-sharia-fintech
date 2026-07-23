# pyright: strict
"""Capstone: unit_of_work.py -- new/dirty/deleted tracking (co-16, co-17, co-18),
parent-before-child flush ordering (co-19), and one atomic transaction per flush (co-20).
Every write goes through query_builder.py (co-01..co-08) -- this module never assembles a
SQL string by hand.
"""

from typing import Any

import query_builder
from domain import Customer, Order
from mapper import customer_to_values, order_to_values
from session import Session


def _to_values(obj: Customer | Order) -> dict[str, Any]:  # => dispatches to the right co-11 mapping function
    if isinstance(obj, Customer):
        return customer_to_values(obj)
    return order_to_values(obj)


def _table_of(obj: Customer | Order) -> str:  # => which table a tracked object belongs to
    return "customer" if isinstance(obj, Customer) else "customer_order"


class UnitOfWork:
    def __init__(self, session: Session) -> None:
        self._session = session  # => co-15: every write below runs through this session's ONE connection
        self._new_customers: list[Customer] = []  # => co-16: parents, flushed FIRST
        self._new_orders: list[tuple[Order, Customer]] = []  # => co-19: each order paired with its NOT-YET-flushed parent
        self._deleted: list[Order] = []  # => co-18: objects registered for removal
        self._tracked: dict[int, Customer | Order] = {}  # => co-17: keyed by id(obj), for dirty comparison
        self._snapshots: dict[int, dict[str, Any]] = {}  # => co-17: the load-time state each tracked object started from

    def register_new_customer(self, customer: Customer) -> None:  # => co-16: tracked, no SQL runs yet
        self._new_customers.append(customer)

    def register_new_order(self, order: Order, customer: Customer) -> None:  # => co-19: parent may still lack a real id
        self._new_orders.append((order, customer))  # => `customer.id` is read again at flush time, once it's real

    def register_deleted(self, order: Order) -> None:  # => co-18: tracked, no SQL runs yet
        self._deleted.append(order)

    def track_clean(self, obj: Customer | Order) -> None:  # => co-17: registers an ALREADY-persisted object
        self._tracked[id(obj)] = obj  # => keeps a reference so dirty_objects() can walk it later
        self._snapshots[id(obj)] = _to_values(obj)  # => the coerced row-shape to compare future mutations against

    def dirty_objects(self) -> list[Customer | Order]:  # => co-17: live state vs load-time snapshot, for every tracked object
        dirty: list[Customer | Order] = []
        for key, obj in self._tracked.items():
            if _to_values(obj) != self._snapshots[key]:  # => co-17: diverged since track_clean() was called
                dirty.append(obj)
        return dirty

    def flush(self) -> None:  # => co-20: every pending write, ONE transaction, commit or roll back together
        conn = self._session.conn
        try:
            for customer in self._new_customers:  # => co-19 step 1: EVERY parent's INSERT runs first
                sql, params = query_builder.insert("customer").values(**customer_to_values(customer)).compile()
                cursor = conn.execute(sql, params)  # => co-08: compile()'s output feeds execute() directly
                assert cursor.lastrowid is not None  # => SQLite always assigns a rowid on a real INSERT
                customer.id = cursor.lastrowid  # => the pk THIS order's FK will read, one loop below
                self._session.identity_map.put("customer", customer.id, customer)  # => co-13: joins the map on flush too

            for order, customer in self._new_orders:  # => co-19 step 2: children run ONLY after their parent, above
                assert customer.id is not None  # => co-19: guaranteed real by this point -- step 1 already ran
                order.customer_id = customer.id  # => co-19: resolved NOW, not when register_new_order() was called
                sql, params = query_builder.insert("customer_order").values(**order_to_values(order)).compile()
                cursor = conn.execute(sql, params)
                assert cursor.lastrowid is not None
                order.id = cursor.lastrowid
                self._session.identity_map.put("customer_order", order.id, order)

            for obj in self.dirty_objects():  # => co-17: only genuinely-changed tracked objects reach here
                live = _to_values(obj)
                snapshot = self._snapshots[id(obj)]
                changed = {col: val for col, val in live.items() if val != snapshot[col]}  # => co-17: the minimal diff
                if changed:  # => an empty diff means nothing to write -- no UPDATE is issued at all
                    assert obj.id is not None  # => a tracked-clean object always has a real pk already
                    sql, params = query_builder.update(_table_of(obj)).set(**changed).where("id", obj.id).compile()
                    conn.execute(sql, params)  # => co-17: the UPDATE's SET clause contains ONLY the changed columns
                self._snapshots[id(obj)] = live  # => refreshes the snapshot so a second flush sees no more dirt

            for order in self._deleted:  # => co-18: every registered-deleted object becomes a real DELETE
                assert order.id is not None
                sql, params = query_builder.delete("customer_order").where("id", order.id).compile()
                conn.execute(sql, params)

            conn.commit()  # => co-20: reached ONLY if every write above succeeded -- all durable together
        except Exception:  # => co-20: ANY failure anywhere above rolls back the WHOLE batch, not just one write
            conn.rollback()
            raise  # => the caller still sees the failure -- rollback does not hide it

        self._new_customers = []  # => co-16: flushed objects are no longer "new"
        self._new_orders = []
        self._deleted = []  # => co-18: flushed deletions are no longer pending
