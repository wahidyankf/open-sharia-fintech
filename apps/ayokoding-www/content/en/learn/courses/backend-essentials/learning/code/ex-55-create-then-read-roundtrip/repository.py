"""Repository module for Example 55: create then read, in one round trip."""

# => co-02/co-14: create_task() and get_task() together prove the WRITE
#    genuinely reaches the SAME file the next call's READ opens, not just memory
from __future__ import annotations  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => the ONLY database driver this module needs -- it ships with Python itself
from pathlib import Path  # => builds an absolute, OS-independent path to the db file

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


def connect() -> sqlite3.Connection:  # => opens and configures one sqlite3 connection
    connection = sqlite3.connect(DB_PATH)  # => DB_PATH is the single file this module reads/writes
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not just row[0]
    return connection  # => the caller owns closing this connection when done


def init_db() -> None:  # => (re)creates the schema, starting EMPTY
    DB_PATH.unlink(missing_ok=True)  # => start every run from a clean, deterministic file
    connection = connect()  # => a fresh connection, scoped to just this setup call
    connection.execute(  # => defines the table's shape -- no seed rows this time
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"  # => the exact DDL
    )  # => starts EMPTY -- this example is entirely about the create-then-read round trip
    connection.commit()  # => without this, the table definition never reaches the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def create_task(title: str) -> int:  # => co-02/co-14: step one of the round trip -- the write half
    # => co-02/co-14: step one of the round trip -- the write half
    connection = connect()  # => a fresh connection, scoped to just this call
    cursor = connection.execute(  # => "?" binds title as DATA, the same safety property as before
        "INSERT INTO tasks (title) VALUES (?)",
        (title,),  # => one placeholder, one bound value
    )  # => "?" binds title as DATA, the same safety property as every earlier example
    connection.commit()  # => without this, the row exists only in this connection's transaction
    new_id = cursor.lastrowid  # => sqlite3 exposes the AUTOINCREMENT id straight off the cursor
    connection.close()  # => releases the connection immediately after writing
    assert new_id is not None  # => guaranteed non-None right after a successful INSERT
    return new_id  # => the id the read half will use to prove persistence


def get_task(task_id: int) -> sqlite3.Row | None:  # => co-02/co-14: step two of the round trip
    # => co-02/co-14: step two of the round trip -- the read half
    connection = connect()  # => a fresh connection, scoped to just this call
    row = connection.execute(  # => a SEPARATE connection from the one create_task() used
        "SELECT id, title FROM tasks WHERE id = ?",
        (task_id,),  # => one placeholder, one bound value
    ).fetchone()  # => a single Row, if the earlier INSERT genuinely persisted
    connection.close()  # => co-24: connection lifetime is scoped to one call, not shared state
    return row  # => propagates the None case straight through to the caller
