# pyright: strict
"""Kata 7 (before): a migration runner with NO schema_version bookkeeping re-applies
every migration on every run -- a second run against an already-migrated database
crashes instead of being a safe no-op (co-24)."""

import contextlib
import sqlite3


def migrate(conn: sqlite3.Connection) -> None:
    # BUG: no tracking table, no "already applied" check -- this DDL runs EVERY call.
    conn.execute("CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    conn.commit()


with contextlib.closing(sqlite3.connect(":memory:")) as conn:
    migrate(conn)  # first run: creates the table -- fine so far
    try:
        migrate(conn)  # intent: a second run (e.g. on app restart) should be a safe no-op
    except sqlite3.OperationalError as exc:
        print(f"OperationalError: {exc}")
