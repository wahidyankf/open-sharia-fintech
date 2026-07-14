"""Repository module for Example 40: update a row in place."""

# => the "U" in CRUD -- this file's job is one function, update_task(), which
#    runs an UPDATE and reports back via rowcount whether a row actually changed
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
    )  # => AUTOINCREMENT guarantees ids only ever go up, never get reused
    connection.executemany(  # => runs the SAME statement once per tuple below
        "INSERT INTO tasks (title) VALUES (?)",  # => one "?" placeholder, bound per tuple
        [("Buy milk",), ("Walk dog",)],  # => two seed rows
    )  # => two seed rows -- id 1 and id 2, both about to be updated
    connection.commit()  # => without this, the inserts never reach the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def update_task(task_id: int, title: str) -> bool:  # => co-14/co-02: UPDATE, not DELETE+INSERT
    connection = connect()  # => a fresh connection, scoped to just this call
    cursor = connection.execute(  # => two "?" placeholders, bound positionally in tuple order
        "UPDATE tasks SET title = ? WHERE id = ?",  # => co-14: parameterized -- never string-formatted
        (title, task_id),  # => title first, then task_id
    )  # => cursor.rowcount below reports how many rows this statement touched
    connection.commit()  # => without this, the change never reaches the file on disk
    changed = cursor.rowcount > 0  # => rowcount is 0 when task_id did not match any row
    connection.close()  # => co-24: connection lifetime is scoped to one call, not shared state
    return changed  # => lets the handler distinguish "updated" from "nothing to update"


def get_task(task_id: int) -> sqlite3.Row | None:  # => used only to PROVE the update landed on disk
    connection = connect()  # => a fresh connection, scoped to just this call
    row = connection.execute(  # => looks up exactly one row by its primary key
        "SELECT id, title FROM tasks WHERE id = ?",  # => co-14: same parameterized pattern throughout
        (task_id,),  # => one placeholder, one bound value
    ).fetchone()  # => a single Row, or None if task_id does not exist
    connection.close()  # => releases the connection immediately after reading
    return row  # => propagates the None case straight through to the caller
