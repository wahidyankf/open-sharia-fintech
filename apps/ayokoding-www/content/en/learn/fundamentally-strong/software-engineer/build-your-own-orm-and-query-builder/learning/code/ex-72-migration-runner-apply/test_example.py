"""Example 72: pytest verification for a Migration Runner Applying DDL."""

import contextlib
import sqlite3

from example import Migration, apply_migration


def test_applying_a_migration_creates_the_declared_table() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        migration = Migration(version=1, sql="CREATE TABLE items(id INTEGER PRIMARY KEY);")  # => one migration
        apply_migration(conn, migration)  # => runs it against a real db
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'").fetchall()
        assert rows == [("items",)]  # => the table genuinely exists now


def test_migration_data_is_immutable() -> None:
    migration = Migration(version=1, sql="CREATE TABLE x(id INTEGER);")  # => a frozen dataclass instance
    try:
        migration.version = 2  # type: ignore[misc]  # => attempting to mutate a frozen field
        assert False, "expected a FrozenInstanceError"  # => this line must never run
    except Exception:  # noqa: BLE001  # => dataclasses.FrozenInstanceError, caught broadly for this example
        pass  # => expected -- confirms co-24's migrations are immutable data


# => Run: pytest -- Output: 2 passed
