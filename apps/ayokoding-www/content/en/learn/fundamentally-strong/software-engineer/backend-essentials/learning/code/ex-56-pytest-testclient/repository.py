"""Repository module for Example 56: backing store for the TestClient demo."""

# => co-22: init_db() below is the function the pytest fixture calls ONCE PER
#    TEST -- that per-test reset is what gives each test its own isolated database
from __future__ import (
    annotations,
)  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => the ONLY database driver this module needs -- it ships with Python itself
from pathlib import Path  # => builds an absolute, OS-independent path to the db file

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


def connect() -> sqlite3.Connection:  # => opens and configures one sqlite3 connection
    connection = sqlite3.connect(DB_PATH)  # => DB_PATH is the single file this module reads/writes
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not just row[0]
    return connection  # => the caller owns closing this connection when done


def init_db() -> None:  # => co-22: called by the pytest FIXTURE, once per test function
    # => co-22: called by the pytest FIXTURE below, once per test function --
    #    that per-test call is what gives each test its own isolated database
    DB_PATH.unlink(missing_ok=True)  # => start every run from a clean, deterministic file
    connection = connect()  # => a fresh connection, scoped to just this setup call
    connection.execute(  # => defines the table's shape -- no seed rows this time
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"  # => the exact DDL
    )  # => starts EMPTY -- every row in this example arrives through create_task() below
    connection.commit()  # => without this, the table definition never reaches the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def create_task(
    title: str,
) -> int:  # => co-14: the INSERT this example's tests exercise
    connection = connect()  # => a fresh connection, scoped to just this call
    cursor = connection.execute(  # => "?" binds title as DATA, the same safety property as before
        "INSERT INTO tasks (title) VALUES (?)",
        (title,),  # => one placeholder, one bound value
    )  # => "?" binds title as DATA, the same safety property as every earlier example
    connection.commit()  # => without this, the row exists only in this connection's transaction
    new_id = cursor.lastrowid  # => sqlite3 exposes the AUTOINCREMENT id straight off the cursor
    connection.close()  # => releases the connection immediately after writing
    assert new_id is not None  # => guaranteed non-None right after a successful INSERT
    return new_id  # => the caller needs this to build the 201 response body


def list_tasks() -> list[sqlite3.Row]:  # => co-14: the SELECT this example's isolation test exercises
    connection = connect()  # => a fresh connection, scoped to just this call
    rows = connection.execute(  # => reads every row, oldest id first
        "SELECT id, title FROM tasks ORDER BY id"  # => no WHERE clause -- returns every row
    ).fetchall()  # => every row, oldest id first
    connection.close()  # => connection lifetime is scoped to one call, not shared state
    return rows  # => raw sqlite3.Row objects -- the handler converts them to dicts
