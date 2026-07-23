"""Repository module for Example 43: apply schema.sql at startup."""  # => module docstring

# => co-15: the schema's SOURCE OF TRUTH is the .sql FILE next to this module,
# => not a Python string -- apply_schema() reads it and runs it as one script
from __future__ import annotations  # => lets sqlite3.Row appear in return-type hints below

import sqlite3  # => the ONLY database driver this module needs -- it ships with Python itself
from pathlib import Path  # => builds absolute, OS-independent paths to the db file and schema.sql

DB_PATH = Path(__file__).parent / "tasks.db"  # => co-14: one fixed db file, next to this module
SCHEMA_PATH = Path(__file__).parent / "schema.sql"  # => co-15: the schema's SOURCE OF TRUTH


def connect() -> sqlite3.Connection:  # => opens and configures one sqlite3 connection
    connection = sqlite3.connect(DB_PATH)  # => DB_PATH is the single file this module reads/writes
    connection.row_factory = sqlite3.Row  # => rows behave like dicts: row["title"], not just row[0]
    return connection  # => the caller owns closing this connection when done


def apply_schema() -> None:  # => co-15: reads and runs schema.sql, once, at startup
    # => co-15: open the .sql file and execute it as a whole script -- the schema's
    # => source of truth is the FILE, not a Python string embedded in this module
    DB_PATH.unlink(missing_ok=True)  # => start every run from a clean, deterministic file
    connection = connect()  # => a fresh connection, scoped to just this migration call
    schema_sql = SCHEMA_PATH.read_text()  # => reads the ENTIRE schema.sql file as one string
    connection.executescript(schema_sql)  # => runs every statement in that file, in file order
    connection.commit()  # => without this, the CREATE TABLE never reaches the file on disk
    connection.close()  # => releases the connection -- apply_schema() is a one-shot setup call


def table_exists(table_name: str) -> bool:  # => co-15: proof the migration genuinely ran
    # => queries SQLite's own catalog table -- proof the migration genuinely ran
    connection = connect()  # => a fresh connection, scoped to just this call
    row = connection.execute(  # => SQLite tracks every table it owns in this catalog table
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",  # => co-14: parameterized
        (table_name,),  # => "?" binds table_name as DATA, not as SQL syntax
    ).fetchone()  # => a matching catalog row, or None if the table does not exist
    connection.close()  # => releases the connection immediately after reading
    return row is not None  # => a plain boolean the startup assertion can check directly
