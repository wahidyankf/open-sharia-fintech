"""Repository module for Example 36: parameterized search."""

from __future__ import annotations  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => co-14: the ONLY database driver this module needs -- ships with Python itself
from pathlib import Path  # => builds an absolute, OS-independent path to the db file

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


def connect() -> sqlite3.Connection:  # => opens and configures one sqlite3 connection
    connection = sqlite3.connect(DB_PATH)  # => DB_PATH is the single file this module reads/writes
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not row[1]
    return connection  # => the caller owns closing this connection when done


def init_db() -> None:  # => (re)creates the schema and seeds two starter rows
    DB_PATH.unlink(missing_ok=True)  # => delete any stale file first -- every run starts clean
    connection = connect()  # => a fresh connection, scoped to just this setup call
    connection.execute(  # => defines the table's shape once, for the whole example
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"  # => the exact DDL
    )  # => AUTOINCREMENT guarantees ids only ever go up, never get reused
    connection.executemany(  # => runs the SAME statement once per tuple below
        "INSERT INTO tasks (title) VALUES (?)",  # => one "?" placeholder, bound per call
        [("Buy milk",), ("Walk dog",)],  # => one row contains "milk", the other does not
    )  # => "?" binds each title as DATA, never as SQL syntax
    connection.commit()  # => without this, the inserts never reach the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def search_by_title(fragment: str) -> list[sqlite3.Row]:  # => a substring search over "title"
    # => co-14/co-20: the "?" PLACEHOLDER, not an f-string, is what makes this safe.
    #    SQLite binds `fragment` as DATA, never as part of the SQL grammar itself,
    #    so it is structurally impossible for fragment to inject a second statement
    connection = connect()  # => a fresh connection, scoped to just this call
    rows = connection.execute(  # => LIKE with wildcards built around the bound value
        "SELECT id, title FROM tasks WHERE title LIKE ? ORDER BY id",  # => the one "?" placeholder
        (f"%{fragment}%",),  # => a TUPLE of bound parameters, matching the one "?"
    ).fetchall()  # => zero or more matching rows, never a raised SQL error
    connection.close()  # => co-24: connection lifetime is scoped to one call, not shared state
    return rows  # => raw sqlite3.Row objects -- possibly empty


def count_tasks() -> int:  # => used only to PROVE the table survived an injection attempt intact
    connection = connect()  # => a fresh connection, scoped to just this call
    (count,) = connection.execute(  # => a single-row, single-column result, unpacked directly
        "SELECT COUNT(*) FROM tasks"  # => no WHERE clause -- counts every row in the table
    ).fetchone()  # => fetchone() -- exactly one row is always returned by COUNT(*)
    connection.close()  # => releases the connection immediately after reading
    return int(count)  # => COUNT(*) already returns an int, but be explicit for the type checker
