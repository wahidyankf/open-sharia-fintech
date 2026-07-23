"""Repository module for Example 35: connects to SQLite and runs a query."""

from __future__ import annotations  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => co-14: the ONLY database driver this module needs -- ships with Python itself
from pathlib import Path  # => builds an absolute, OS-independent path to the db file

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


def connect() -> sqlite3.Connection:  # => opens and configures one sqlite3 connection
    # => a NEW connection every call -- sqlite3.Connection objects are not
    #    safe to share across threads, so nothing here caches one
    connection = sqlite3.connect(DB_PATH)  # => DB_PATH is the single file this module reads/writes
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not row[1]
    return connection  # => the caller owns closing this connection when done


def init_db() -> None:  # => (re)creates the schema and seeds two starter rows
    # => co-14/co-24: schema + seed data live ONLY in the repository module,
    #    never in app.py -- the handler will not even know this function exists
    DB_PATH.unlink(missing_ok=True)  # => delete any stale file first -- every run starts clean
    connection = connect()  # => a fresh connection, scoped to just this setup call
    connection.execute(  # => defines the table's shape once, for the whole example
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"  # => the exact DDL
    )  # => AUTOINCREMENT guarantees ids only ever go up, never get reused
    connection.executemany(  # => runs the SAME statement once per tuple below
        "INSERT INTO tasks (title) VALUES (?)",
        [("Buy milk",), ("Walk dog",)],  # => two seed rows for list_tasks() to return
    )  # => "?" binds each title as DATA, never as SQL syntax
    connection.commit()  # => without this, the inserts never reach the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def list_tasks() -> list[sqlite3.Row]:  # => co-14: the ONLY function that runs a SELECT
    connection = connect()  # => a fresh connection, scoped to just this call
    rows = connection.execute(  # => reads every row, oldest id first
        "SELECT id, title FROM tasks ORDER BY id"  # => no WHERE clause -- returns every row
    ).fetchall()  # => fetchall() -- a plain list of every matching Row
    connection.close()  # => co-24: connection lifetime is scoped to one call, not shared state
    return rows  # => raw sqlite3.Row objects -- the handler converts them to dicts
