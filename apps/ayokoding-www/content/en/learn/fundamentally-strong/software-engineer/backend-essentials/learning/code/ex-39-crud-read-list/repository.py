"""Repository module for Example 39: read the whole list."""

# => the "R" (plural) in CRUD -- create_task() grows the table, list_tasks()
#    reads every row back, so this one file proves both halves compose
from __future__ import annotations  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => co-14: the ONLY database driver this module needs -- ships with Python itself
from pathlib import Path  # => builds an absolute, OS-independent path to the db file

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


def connect() -> sqlite3.Connection:  # => opens and configures one sqlite3 connection
    connection = sqlite3.connect(DB_PATH)  # => DB_PATH is the single file this module reads/writes
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not row[1]
    return connection  # => the caller owns closing this connection when done


def init_db() -> None:  # => (re)creates the schema, starting EMPTY
    DB_PATH.unlink(missing_ok=True)  # => delete any stale file first -- every run starts clean
    connection = connect()  # => a fresh connection, scoped to just this setup call
    connection.execute(  # => defines the table's shape -- no seed rows this time
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"  # => the exact DDL
    )  # => starts EMPTY -- every row here arrives through create_task() below
    connection.commit()  # => without this, the table definition never reaches the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def create_task(title: str) -> int:  # => co-14: reused so curl/pytest can grow the list first
    connection = connect()  # => a fresh connection, scoped to just this call
    cursor = connection.execute(  # => "?" binds title as DATA, the same property as every example
        "INSERT INTO tasks (title) VALUES (?)",
        (title,),  # => one placeholder, one bound value
    )  # => cursor.lastrowid below reads the id SQLite just assigned
    connection.commit()  # => without this, the row exists only in this connection's transaction
    new_id = cursor.lastrowid  # => sqlite3 exposes the AUTOINCREMENT id straight off the cursor
    connection.close()  # => releases the connection immediately after writing
    assert new_id is not None  # => guaranteed non-None right after a successful INSERT
    return new_id  # => the caller needs this to build the 201 response body


def list_tasks() -> list[sqlite3.Row]:  # => co-14: every row, in insertion order -- the "R" of CRUD
    connection = connect()  # => a fresh connection, scoped to just this call
    rows = connection.execute(  # => reads every row, oldest id first
        "SELECT id, title FROM tasks ORDER BY id"  # => no WHERE clause -- returns every row
    ).fetchall()  # => fetchall() -- a plain list of every matching Row
    connection.close()  # => co-24: connection lifetime is scoped to one call, not shared state
    return rows  # => raw sqlite3.Row objects -- the handler converts them to dicts
