"""Example 73: pytest verification for a schema_version Bookkeeping Table."""

import contextlib
import sqlite3

from example import Migration, already_applied, apply_migration, ensure_version_table


def test_a_migration_is_only_applied_once() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        ensure_version_table(conn)  # => bookkeeping table set up
        migration = Migration(version=1, sql="CREATE TABLE items(id INTEGER PRIMARY KEY);")  # => one migration
        apply_migration(conn, migration)  # => applies AND records
        apply_migration(conn, migration)  # => re-run -- must be a no-op
        count = conn.execute("SELECT COUNT(*) FROM schema_version").fetchone()[0]
        assert count == 1  # => never double-recorded


def test_already_applied_reflects_the_version_table_accurately() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        ensure_version_table(conn)
        assert already_applied(conn, 5) is False  # => nothing recorded yet
        apply_migration(conn, Migration(version=5, sql="CREATE TABLE t(id INTEGER);"))
        assert already_applied(conn, 5) is True  # => now recorded


# => Run: pytest -- Output: 2 passed
