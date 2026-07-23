"""Repository module for Example 37: insert a new row."""

# => the "C" in CRUD -- this file's job is one function, create_task(), and
#    every INSERT detail for the whole example lives right here, nowhere else
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
    )  # => starts EMPTY -- this example is entirely about the create path
    connection.commit()  # => without this, the table definition never reaches the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def create_task(title: str) -> int:  # => co-14/co-08: the ONLY function that runs an INSERT
    connection = connect()  # => a fresh connection, scoped to just this call
    cursor = connection.execute(  # => "?" binds title as DATA, the safety property from Example 36
        "INSERT INTO tasks (title) VALUES (?)",
        (title,),  # => one placeholder, one bound value
    )  # => cursor.lastrowid below reads the id SQLite just assigned
    connection.commit()  # => without this, the row exists only in this connection's transaction
    new_id = cursor.lastrowid  # => sqlite3 exposes the AUTOINCREMENT id straight off the cursor
    connection.close()  # => co-24: connection lifetime is scoped to one call, not shared state
    assert new_id is not None  # => guaranteed non-None right after a successful INSERT
    return new_id  # => the caller needs this to build the 201 response body


def get_task(task_id: int) -> sqlite3.Row | None:  # => used only to PROVE persistence
    connection = connect()  # => a fresh connection, scoped to just this call
    row = connection.execute(  # => looks up exactly one row by its primary key
        "SELECT id, title FROM tasks WHERE id = ?",
        (task_id,),  # => one placeholder, one bound value
    ).fetchone()  # => a single Row, or None if task_id does not exist
    connection.close()  # => releases the connection immediately after reading
    return row  # => propagates the None case straight through to the caller
