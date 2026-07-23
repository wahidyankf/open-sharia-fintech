"""Repository module for Example 47: SQL functions that accept an injected connection."""

# => co-23: get_connection() is a GENERATOR dependency -- FastAPI runs the code
#    before "yield" per request and GUARANTEES the "finally" cleanup runs after
from __future__ import annotations  # => lets sqlite3.Connection appear in signatures below

import sqlite3  # => the ONLY database driver this module needs -- it ships with Python itself
from collections.abc import Iterator  # => the return type a generator dependency needs
from pathlib import Path  # => builds an absolute, OS-independent path to the db file

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


def init_db() -> None:  # => (re)creates the schema and seeds two starter rows
    DB_PATH.unlink(missing_ok=True)  # => start every run from a clean, deterministic file
    connection = sqlite3.connect(DB_PATH)  # => a ONE-OFF connection, used only for setup
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not just row[0]
    connection.execute(  # => defines the table's shape once, for the whole example
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"  # => the exact DDL
    )  # => defines the table's shape once, for the whole example
    connection.executemany(  # => runs the SAME statement once per tuple below
        "INSERT INTO tasks (title) VALUES (?)",
        [("Buy milk",), ("Walk dog",)],  # => two seed rows
    )  # => two seed rows so list_tasks() below has something real to return
    connection.commit()  # => without this, the inserts never reach the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def get_connection() -> Iterator[sqlite3.Connection]:  # => co-23: FastAPI drives this per request
    # => co-23: a GENERATOR dependency -- code before "yield" runs per request,
    #    code after "yield" runs once the response is done (guaranteed cleanup)
    connection = sqlite3.connect(DB_PATH)  # => one connection, opened fresh for THIS request
    connection.row_factory = sqlite3.Row  # => rows behave like dicts for every caller downstream
    try:  # => co-23: guarantees the connection closes even if the handler raises
        yield connection  # => the handler receives exactly THIS object as its argument
    finally:  # => runs on both the success path AND the exception path
        connection.close()  # => runs even if the handler raised an exception


def list_tasks(connection: sqlite3.Connection) -> list[sqlite3.Row]:  # => connection is a PARAMETER
    # => co-14: STILL the only place with a SELECT -- it just receives an
    #    already-open connection instead of opening its own, like earlier examples did
    return connection.execute(  # => no connect() call here -- the caller already supplied one
        "SELECT id, title FROM tasks ORDER BY id"  # => no WHERE clause -- returns every row
    ).fetchall()  # => every row, oldest id first -- no connect()/close() needed here
