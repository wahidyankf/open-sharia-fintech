"""Repository module for Example 42: update/delete against a missing id."""  # => module docstring

# => the SAME update_task()/delete_task() shape as ex-40/ex-41, seeded with
# => only ONE row this time so most ids the app queries are genuinely missing
from __future__ import annotations  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => the ONLY database driver this module needs -- it ships with Python itself
from pathlib import Path  # => builds an absolute, OS-independent path to the db file

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


def connect() -> sqlite3.Connection:  # => opens and configures one sqlite3 connection
    connection = sqlite3.connect(DB_PATH)  # => DB_PATH is the single file this module reads/writes
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not just row[0]
    return connection  # => the caller owns closing this connection when done


def init_db() -> None:  # => (re)creates the schema and seeds exactly ONE starter row
    DB_PATH.unlink(missing_ok=True)  # => start every run from a clean, deterministic file
    connection = connect()  # => a fresh connection, scoped to just this setup call
    connection.execute(  # => defines the table's shape once, for the whole example
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"  # => the exact DDL
    )  # => AUTOINCREMENT guarantees ids only ever go up, never get reused
    connection.execute(  # => runs the INSERT exactly once, unlike executemany() elsewhere
        "INSERT INTO tasks (title) VALUES (?)",
        ("Buy milk",),  # => one seed row
    )  # => one seed row, id 1 -- every id this example queries besides 1 is missing
    connection.commit()  # => without this, the insert never reaches the file on disk
    connection.close()  # => releases the connection -- init_db() is a one-shot setup call


def update_task(task_id: int, title: str) -> bool:  # => co-14/co-02: identical shape to ex-40
    connection = connect()  # => a fresh connection, scoped to just this call
    cursor = connection.execute(  # => two "?" placeholders, bound positionally in tuple order
        "UPDATE tasks SET title = ? WHERE id = ?",
        (title, task_id),  # => title first, then task_id
    )  # => cursor.rowcount below reports how many rows this statement touched
    connection.commit()  # => without this, the change never reaches the file on disk
    changed = cursor.rowcount > 0  # => rowcount is 0 when task_id did not match any row
    connection.close()  # => co-24: connection lifetime is scoped to one call, not shared state
    return changed  # => drives the app-level TaskNotFoundError below


def delete_task(task_id: int) -> bool:  # => co-14: identical shape to ex-41's delete_task
    connection = connect()  # => a fresh connection, scoped to just this call
    cursor = connection.execute(  # => "?" binds task_id as DATA, never as literal SQL text
        "DELETE FROM tasks WHERE id = ?",
        (task_id,),  # => one placeholder, one bound value
    )  # => cursor.rowcount below reports how many rows this statement touched
    connection.commit()  # => without this, the deletion never reaches the file on disk
    removed = cursor.rowcount > 0  # => rowcount is 0 when task_id did not match any row
    connection.close()  # => releases the connection immediately after writing
    return removed  # => drives the SAME app-level TaskNotFoundError as update_task above
