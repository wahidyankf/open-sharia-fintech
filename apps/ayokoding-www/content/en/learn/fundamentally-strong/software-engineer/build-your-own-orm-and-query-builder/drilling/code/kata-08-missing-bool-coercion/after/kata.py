# pyright: strict
"""Kata 8 (after): coerce the raw 0/1 INTEGER to a real bool with `bool(row[2])` at load
time -- `is True` now works because the mapped attribute is genuinely a bool object (co-12)."""

import contextlib
import dataclasses
import sqlite3


@dataclasses.dataclass
class Customer:
    id: int
    name: str
    active: bool


def load(row: tuple[int, str, int]) -> Customer:
    return Customer(id=row[0], name=row[1], active=bool(row[2]))  # THE FIX: bool() coercion


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT, active INTEGER)")
    conn.execute("INSERT INTO customer VALUES (1, 'Ada', 1)")
    conn.commit()
    row = conn.execute("SELECT id, name, active FROM customer WHERE id = 1").fetchone()
    customer = load(row)
    print(type(customer.active).__name__, customer.active is True)
