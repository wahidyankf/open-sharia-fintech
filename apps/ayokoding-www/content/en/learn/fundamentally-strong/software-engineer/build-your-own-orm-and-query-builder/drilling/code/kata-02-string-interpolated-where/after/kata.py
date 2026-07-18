# pyright: strict
"""Kata 2 (after): a bound "?" placeholder treats the value as pure data -- the SQL text
never changes shape no matter what the value contains (co-02)."""

import contextlib
import sqlite3


def find_by_name(conn: sqlite3.Connection, name: str) -> list[tuple[int, str]]:
    # THE FIX: the value is bound as a parameter -- never part of the SQL text at all.
    sql = "SELECT id, name FROM customer WHERE name = ?"
    return conn.execute(sql, (name,)).fetchall()


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT)")
    conn.executemany("INSERT INTO customer(name) VALUES (?)", [("Ada",), ("Bob",)])
    conn.commit()

    hostile = "x' OR '1'='1"  # the EXACT same value -- now inert, treated as literal data
    rows = find_by_name(conn, hostile)
    print(rows)
