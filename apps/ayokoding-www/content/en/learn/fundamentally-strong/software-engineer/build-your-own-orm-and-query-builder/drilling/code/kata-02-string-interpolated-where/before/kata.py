# pyright: strict
"""Kata 2 (before): building WHERE with an f-string interpolates the value directly
into the SQL text -- a value containing SQL syntax changes what the statement DOES (co-02)."""

import contextlib
import sqlite3


def find_by_name(conn: sqlite3.Connection, name: str) -> list[tuple[int, str]]:
    # BUG: the value is interpolated straight into the SQL text, not bound as a parameter.
    sql = f"SELECT id, name FROM customer WHERE name = '{name}'"
    return conn.execute(sql).fetchall()


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT)")
    conn.executemany("INSERT INTO customer(name) VALUES (?)", [("Ada",), ("Bob",)])
    conn.commit()

    # intent: look up a customer whose name genuinely contains a single quote.
    hostile = "x' OR '1'='1"  # a value that is ALSO valid SQL syntax once interpolated
    rows = find_by_name(conn, hostile)
    print(rows)
