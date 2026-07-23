# pyright: strict
"""Kata 7 (after): a schema_version tracking table records what already ran, so a second
call against an already-migrated database skips the DDL entirely -- a genuine no-op (co-24)."""

import contextlib
import sqlite3


def migrate(conn: sqlite3.Connection) -> list[int]:
    conn.execute("CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY)")  # THE FIX
    applied = {row[0] for row in conn.execute("SELECT version FROM schema_version").fetchall()}
    newly_applied: list[int] = []
    if 1 not in applied:  # THE FIX: only runs the DDL if version 1 hasn't been recorded yet
        conn.execute("CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        conn.execute("INSERT INTO schema_version VALUES (1)")
        newly_applied.append(1)
    conn.commit()
    return newly_applied


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    first = migrate(conn)
    second = migrate(conn)  # a genuine no-op -- no OperationalError, nothing re-applied
    print(first, second)
