# pyright: strict
"""Kata 8 (before): SQLite has no native boolean type -- it stores 0/1 integers. Mapping a
row WITHOUT coercing that integer to a real bool means `is True` (identity, not equality)
silently fails even for a row that is genuinely "active" (co-12)."""

import contextlib
import dataclasses
import sqlite3


@dataclasses.dataclass
class Customer:
    id: int
    name: str
    active: bool


def load(row: tuple[int, str, int]) -> Customer:
    # BUG: row[2] is SQLite's raw 0/1 INTEGER, assigned directly -- never coerced to bool.
    return Customer(id=row[0], name=row[1], active=row[2])  # type: ignore[arg-type]


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT, active INTEGER)")
    conn.execute("INSERT INTO customer VALUES (1, 'Ada', 1)")  # 1 means "active" in this schema
    conn.commit()
    row = conn.execute("SELECT id, name, active FROM customer WHERE id = 1").fetchone()
    customer = load(row)
    # intent: Ada IS active -- this check should pass.
    print(type(customer.active).__name__, customer.active is True)
