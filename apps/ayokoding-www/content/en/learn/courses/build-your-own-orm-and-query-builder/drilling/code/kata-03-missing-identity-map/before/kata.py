# pyright: strict
"""Kata 3 (before): loading the same primary key twice with NO identity map produces
TWO separate objects that silently drift apart the moment either one is mutated (co-13)."""

import contextlib
import dataclasses
import sqlite3


@dataclasses.dataclass
class Customer:
    id: int
    name: str


def load(conn: sqlite3.Connection, pk: int) -> Customer:
    # BUG: every call runs a fresh query and builds a BRAND NEW object -- no cache anywhere.
    row = conn.execute("SELECT id, name FROM customer WHERE id = ?", (pk,)).fetchone()
    return Customer(id=row[0], name=row[1])


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO customer VALUES (1, 'Ada')")
    conn.commit()

    # intent: two "loads" of the same row, in two different parts of a program, should
    # see the SAME in-memory state once one of them is renamed.
    a = load(conn, 1)
    b = load(conn, 1)
    a.name = "Ada Renamed"  # mutates ONLY a's copy -- the database itself is untouched here
    print(a is b, a.name, b.name)
