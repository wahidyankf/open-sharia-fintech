"""Example 73: A schema_version Table Records Which Migrations Already Ran."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the migration's own data shape
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-24: a migration is immutable data
class Migration:  # => the smallest unit a migration runner applies
    version: int  # => co-24: uniquely identifies this migration in schema_version
    sql: str  # => the raw DDL this migration executes when applied


def ensure_version_table(conn: sqlite3.Connection) -> None:  # => co-24: the bookkeeping table itself
    conn.execute("CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY)")  # => idempotent DDL
    conn.commit()  # => makes the bookkeeping table durable before anything else runs


def already_applied(conn: sqlite3.Connection, version: int) -> bool:  # => co-24: the re-run guard
    row = conn.execute("SELECT 1 FROM schema_version WHERE version = ?", (version,)).fetchone()  # => real lookup
    return row is not None  # => True only if THIS version's row already exists in schema_version


def apply_migration(conn: sqlite3.Connection, migration: Migration) -> None:  # => co-24: apply-then-record
    if already_applied(conn, migration.version):  # => co-24: SKIPS migrations already recorded as applied
        return  # => a no-op -- re-running this migration a second time changes nothing
    conn.executescript(migration.sql)  # => runs the migration's own DDL
    conn.execute("INSERT INTO schema_version VALUES (?)", (migration.version,))  # => co-24: records it as applied
    conn.commit()  # => makes BOTH the schema change and its bookkeeping row durable together


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    ensure_version_table(conn)  # => co-24: sets up the bookkeeping table first
    create_users = Migration(version=1, sql="CREATE TABLE users(id INTEGER PRIMARY KEY);")  # => one migration
    assert not already_applied(conn, 1)  # => confirmed: not yet recorded, before the first apply
    apply_migration(conn, create_users)  # => co-24: runs it AND records version 1 as applied
    assert already_applied(conn, 1)  # => co-24: NOW recorded -- the version table reflects reality
    apply_migration(conn, create_users)  # => a SECOND attempt at the SAME migration -- must be a no-op
    count = conn.execute("SELECT COUNT(*) FROM schema_version").fetchone()[0]  # => proves no duplicate record
    assert count == 1  # => co-24: still exactly ONE row -- re-running never double-records a version
    print(count)  # => Output: 1
