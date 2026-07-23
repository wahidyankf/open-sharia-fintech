# pyright: strict
"""Kata 3 (after): a per-session {pk: object} cache guarantees the SECOND load of the SAME
primary key returns the IDENTICAL object the first load already produced (co-13)."""

import contextlib
import dataclasses
import sqlite3


@dataclasses.dataclass
class Customer:
    id: int
    name: str


class IdentityMap:  # THE FIX: a cache keyed by primary key, checked BEFORE any new object is built
    def __init__(self) -> None:
        self._cache: dict[int, Customer] = {}

    def load(self, conn: sqlite3.Connection, pk: int) -> Customer:
        if pk in self._cache:  # a cache HIT -- return the SAME object, no query at all
            return self._cache[pk]
        row = conn.execute("SELECT id, name FROM customer WHERE id = ?", (pk,)).fetchone()
        customer = Customer(id=row[0], name=row[1])
        self._cache[pk] = customer  # registered BEFORE returning -- the NEXT load() call hits this entry
        return customer


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO customer VALUES (1, 'Ada')")
    conn.commit()

    identity_map = IdentityMap()
    a = identity_map.load(conn, 1)
    b = identity_map.load(conn, 1)
    a.name = "Ada Renamed"  # mutates the ONE shared object -- b sees it too, because a IS b
    print(a is b, a.name, b.name)
