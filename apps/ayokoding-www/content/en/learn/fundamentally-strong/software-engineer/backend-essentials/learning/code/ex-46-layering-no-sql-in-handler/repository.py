"""Repository module for Example 46: the only place SQL is allowed to live."""

# => co-24: every query keyword this whole example ever uses lives in THIS
#    file -- app.py's own test proves it by inspecting app.py's source text
from __future__ import annotations  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => the ONLY database driver this module needs -- it ships with Python itself
from pathlib import Path  # => builds an absolute, OS-independent path to the db file

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


def connect() -> sqlite3.Connection:  # => opens and configures one sqlite3 connection
    connection = sqlite3.connect(DB_PATH)  # => DB_PATH is the single file this module reads/writes
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not just row[0]
    return connection  # => the caller owns closing this connection when done


def init_db() -> None:  # => (re)creates the schema and seeds two starter rows
    DB_PATH.unlink(missing_ok=True)  # => start every run from a clean, deterministic file
    connection = connect()  # => a fresh connection, scoped to just this setup call
    connection.execute(  # => defines the table's shape once, for the whole example
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"  # => the exact DDL
    )  # => defines the table's shape once, for the whole example
    connection.executemany(  # => runs the SAME statement once per tuple below
        "INSERT INTO tasks (title) VALUES (?)",
        [("Buy milk",), ("Walk dog",)],  # => two seed rows
    )  # => two seed rows so list_tasks() below has something real to return
    connection.commit()  # => without this, the inserts never reach the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def list_tasks() -> list[sqlite3.Row]:  # => co-24: the ONLY function in the example with a query
    # => co-24: this query is the ONLY data-access statement in the entire example --
    #    app.py never sees it, never imports sqlite3, never writes a query string
    connection = connect()  # => a fresh connection, scoped to just this call
    rows = connection.execute(  # => the one and only place this whole example reads data
        "SELECT id, title FROM tasks ORDER BY id"  # => no WHERE clause -- returns every row
    ).fetchall()  # => every row, oldest id first
    connection.close()  # => connection lifetime is scoped to one call, not shared state
    return rows  # => raw sqlite3.Row objects -- the handler converts them to dicts
