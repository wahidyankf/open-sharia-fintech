"""Repository + migration module for Example 44."""

# => co-15: an ADDITIVE migration -- create_v1_schema() seeds the OLD shape,
#    migrate_add_priority_column() adds a column AND backfills existing rows
from __future__ import annotations  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => the ONLY database driver this module needs -- it ships with Python itself
from pathlib import Path  # => builds an absolute, OS-independent path to the db file

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module


def connect() -> sqlite3.Connection:  # => opens and configures one sqlite3 connection
    connection = sqlite3.connect(DB_PATH)  # => DB_PATH is the single file this module reads/writes
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not just row[0]
    return connection  # => the caller owns closing this connection when done


def create_v1_schema() -> None:  # => co-15: the ORIGINAL schema, before this migration runs
    # => co-15: the ORIGINAL schema, before this example's migration ever runs
    DB_PATH.unlink(missing_ok=True)  # => start every run from a clean, deterministic file
    connection = connect()  # => a fresh connection, scoped to just this setup call
    connection.execute(  # => v1 DDL -- deliberately narrower than the post-migration shape
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"  # => the exact v1 DDL
    )  # => v1: only (id, title) -- no "priority" column exists yet
    connection.execute(  # => runs BEFORE migrate_add_priority_column() below ever executes
        "INSERT INTO tasks (title) VALUES (?)",
        ("Buy milk",),  # => one pre-migration row
    )  # => a row inserted BEFORE the "priority" column exists at all
    connection.commit()  # => without this, the insert never reaches the file on disk
    connection.close()  # => releases the connection -- create_v1_schema() is a one-shot call


def migrate_add_priority_column() -> None:  # => co-15: additive ALTER TABLE + backfill UPDATE
    # => co-15: ADDITIVE only -- never drops or renames the existing "title" column
    connection = connect()  # => a fresh connection, scoped to just this migration call
    connection.execute(  # => co-15: ADD COLUMN never touches an existing column or row's data
        "ALTER TABLE tasks ADD COLUMN priority INTEGER"  # => the exact additive DDL
    )  # => new column; every existing row gets NULL here, including the one above
    connection.execute(  # => co-15: the explicit BACKFILL step, run right after the ALTER
        "UPDATE tasks SET priority = 3 WHERE priority IS NULL"  # => only touches the NULL rows
    )  # => the explicit BACKFILL step -- gives every pre-existing row a real value
    connection.commit()  # => without this, neither the ALTER nor the backfill persists to disk
    connection.close()  # => releases the connection -- migrate_add_priority_column() is one-shot


def column_names() -> set[str]:  # => introspects the live schema, used to PROVE the migration ran
    # => introspects the live schema -- used to PROVE the column was absent, then present
    connection = connect()  # => a fresh connection, scoped to just this call
    info = connection.execute(  # => SQLite's own metadata pragma, no separate driver call needed
        "PRAGMA table_info(tasks)"  # => not parameterized -- table names cannot be bound with "?"
    ).fetchall()  # => one row per column, each with a "name" field
    connection.close()  # => releases the connection immediately after reading
    return {row["name"] for row in info}  # => a set is the right shape for a fast "in" check


def get_task(task_id: int) -> sqlite3.Row | None:  # => used only to PROVE the backfilled value
    connection = connect()  # => a fresh connection, scoped to just this call
    row = connection.execute(  # => reads the POST-migration shape, including "priority"
        "SELECT id, title, priority FROM tasks WHERE id = ?",
        (task_id,),  # => one bound value
    ).fetchone()  # => includes the BACKFILLED "priority" column, post-migration
    connection.close()  # => releases the connection immediately after reading
    return row  # => propagates the None case straight through to the caller
