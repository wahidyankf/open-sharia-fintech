# pyright: strict
"""Capstone: migrations.py -- an ordered, versioned migration runner (co-24). Applying it
twice is a safe no-op: a schema_version table records which migrations already ran, and this
file's own demo below proves the second call changes nothing.
"""

import dataclasses
import sqlite3


@dataclasses.dataclass(frozen=True)  # => co-24: a migration is immutable data, applied in ascending order
class Migration:
    version: int
    sql: str


MIGRATIONS: tuple[Migration, ...] = (
    Migration(
        version=1,
        sql="CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE);",
    ),  # => co-24: the parent table, migration 1 -- UNIQUE email lets run_scenario.py force a REAL rollback (co-20)
    Migration(
        version=2,
        sql=(
            "CREATE TABLE customer_order(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customer(id), item TEXT NOT NULL, amount REAL NOT NULL, placed_on TEXT NOT NULL);"
        ),  # => co-24: the child table, migration 2 -- depends on customer already existing
    ),
)


def migrate(conn: sqlite3.Connection, migrations: tuple[Migration, ...] = MIGRATIONS) -> list[int]:
    conn.execute("CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY)")  # => bookkeeping table
    applied = {row[0] for row in conn.execute("SELECT version FROM schema_version").fetchall()}  # => already-run
    newly_applied: list[int] = []  # => co-24: reported back so callers can prove a re-run is a no-op
    for migration in sorted(migrations, key=lambda m: m.version):  # => co-24: ascending order, always
        if migration.version not in applied:  # => co-24: SKIPS anything already recorded
            conn.executescript(migration.sql)  # => runs THIS migration's own DDL
            conn.execute("INSERT INTO schema_version VALUES (?)", (migration.version,))  # => records it
            newly_applied.append(migration.version)  # => tracked for the caller to inspect
    conn.commit()  # => makes every applied migration (and the bookkeeping row) durable together
    return newly_applied


if __name__ == "__main__":  # => guards against running the demo on `import migrations`
    import contextlib

    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        first = migrate(conn)
        print(first)  # => Output: [1, 2]
        second = migrate(conn)  # => co-24: re-running against an already-migrated database
        print(second)  # => Output: []
        assert second == []  # => co-24: a safe no-op -- nothing left to apply
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        assert {"customer", "customer_order", "schema_version"} <= tables  # => every table genuinely exists
