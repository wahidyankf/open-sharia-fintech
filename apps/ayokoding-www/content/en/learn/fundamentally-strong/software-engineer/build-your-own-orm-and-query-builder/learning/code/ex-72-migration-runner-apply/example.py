"""Example 72: A Migration Runner Applies a DDL Script Against a Real Database."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the migration's own data shape
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-24: a migration is immutable data -- id, description, and SQL
class Migration:  # => the smallest unit a migration runner applies
    version: int  # => co-24: orders migrations -- lower versions apply BEFORE higher ones
    sql: str  # => the raw DDL this migration executes when applied


def apply_migration(conn: sqlite3.Connection, migration: Migration) -> None:  # => co-24: runs ONE migration
    conn.executescript(migration.sql)  # => executescript allows multiple statements in one migration's SQL
    conn.commit()  # => co-24: makes this migration's schema change durable before returning


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    create_users = Migration(  # => co-24: the FIRST migration this database will ever run
        version=1,  # => version 1 -- applied first, by convention
        sql="CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);",  # => the actual DDL to run
    )  # => a complete, immutable migration record
    tables_before = conn.execute(  # => confirms the table does NOT exist yet, before applying
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"  # => sqlite's own catalog table
    ).fetchall()  # => empty -- proves the schema hasn't been created yet
    assert tables_before == []  # => genuinely absent before the migration runs
    apply_migration(conn, create_users)  # => co-24: runs the migration against the REAL database
    tables_after = conn.execute(  # => confirms the table NOW exists, after applying
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"  # => the SAME catalog query
    ).fetchall()  # => one row -- proves the migration actually ran
    assert tables_after == [("users",)]  # => co-24: the real schema now has the table this migration created
    print(len(tables_after))  # => Output: 1
