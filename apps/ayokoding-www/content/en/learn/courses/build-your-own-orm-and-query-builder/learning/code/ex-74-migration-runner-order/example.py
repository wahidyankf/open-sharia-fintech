"""Example 74: A Migration Runner Applies Pending Migrations in Ascending Version Order."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the migration's own data shape
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-24: a migration is immutable data
class Migration:  # => the smallest unit a migration runner applies
    version: int  # => co-24: the sort key -- runner applies these in ASCENDING order, never as-given
    sql: str  # => the raw DDL this migration executes when applied


def ensure_version_table(conn: sqlite3.Connection) -> None:  # => co-24: the bookkeeping table itself
    conn.execute("CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY)")  # => idempotent DDL
    conn.commit()  # => makes the bookkeeping table durable before anything else runs


def applied_versions(conn: sqlite3.Connection) -> set[int]:  # => co-24: every version already recorded
    rows = conn.execute("SELECT version FROM schema_version").fetchall()  # => real lookup, ALL recorded versions
    return {row[0] for row in rows}  # => a set for fast "already applied?" membership checks below


def run_pending(conn: sqlite3.Connection, migrations: list[Migration]) -> list[int]:  # => co-24: the ordering step
    applied = applied_versions(conn)  # => co-24: what's ALREADY been recorded, before this run starts
    pending = sorted(  # => co-24: sorted by version, REGARDLESS of the input list's own order
        (m for m in migrations if m.version not in applied),  # => filters out ALREADY-applied versions first
        key=lambda m: m.version,  # => co-24: the sort key -- ascending by version, nothing else
    )  # => ascending version order -- the runner NEVER trusts caller-supplied ordering
    applied_order: list[int] = []  # => records the ACTUAL application order this run produced
    for migration in pending:  # => co-24: applies STRICTLY in ascending version order
        conn.executescript(migration.sql)  # => runs this migration's own DDL
        conn.execute("INSERT INTO schema_version VALUES (?)", (migration.version,))  # => records it as applied
        applied_order.append(migration.version)  # => co-24: proves the order this run actually used
    conn.commit()  # => makes every applied migration durable together
    return applied_order  # => the sequence this run actually followed, for the caller to inspect


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    ensure_version_table(conn)  # => co-24: sets up the bookkeeping table first
    out_of_order = [  # => co-24: deliberately supplied OUT of version order -- 3, 1, 2
        Migration(version=3, sql="CREATE TABLE orders(id INTEGER PRIMARY KEY);"),  # => version 3, listed FIRST
        Migration(version=1, sql="CREATE TABLE customers(id INTEGER PRIMARY KEY);"),  # => version 1, listed SECOND
        Migration(version=2, sql="CREATE TABLE addresses(id INTEGER PRIMARY KEY);"),  # => version 2, listed THIRD
    ]  # => the runner must ignore this order entirely
    order_applied = run_pending(conn, out_of_order)  # => co-24: the runner SORTS before applying
    assert order_applied == [1, 2, 3]  # => co-24: applied ascending -- 1, then 2, then 3, NOT the input order
    print(order_applied)  # => Output: [1, 2, 3]
