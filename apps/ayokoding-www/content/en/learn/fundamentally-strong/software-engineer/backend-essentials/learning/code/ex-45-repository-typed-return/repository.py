"""Repository module for Example 45: typed return values."""

# => co-24: every function below returns TaskRow, never a bare dict or a raw
#    sqlite3.Row -- pyright can check the contract at the repository boundary
from __future__ import annotations  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => the ONLY database driver this module needs -- it ships with Python itself
from pathlib import Path  # => builds an absolute, OS-independent path to the db file
from typing import TypedDict  # => defines a precise, checkable dict shape

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


class TaskRow(TypedDict):  # => co-24: a precise, checkable shape instead of a bare dict
    id: int  # => pyright flags a missing or mistyped "id" key at edit time
    title: str  # => pyright flags a missing or mistyped "title" key at edit time


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


def _to_task_row(row: sqlite3.Row) -> TaskRow:  # => co-14: the ONE conversion point in this module
    # => co-14: the ONE place a raw sqlite3.Row becomes the typed TaskRow shape
    return TaskRow(id=row["id"], title=row["title"])  # => explicit keyword construction, type-checked


def list_tasks() -> list[TaskRow]:  # => co-24: the return type IS TaskRow, not sqlite3.Row
    connection = connect()  # => a fresh connection, scoped to just this call
    rows = connection.execute(  # => reads every row, oldest id first, as raw sqlite3.Row objects
        "SELECT id, title FROM tasks ORDER BY id"  # => no WHERE clause -- returns every row
    ).fetchall()  # => every row, oldest id first
    connection.close()  # => co-24: connection lifetime is scoped to one call, not shared state
    return [_to_task_row(row) for row in rows]  # => every caller gets TaskRow, never sqlite3.Row
