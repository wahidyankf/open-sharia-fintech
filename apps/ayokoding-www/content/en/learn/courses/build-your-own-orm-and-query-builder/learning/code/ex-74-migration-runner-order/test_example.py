"""Example 74: pytest verification for Ascending-Version Migration Ordering."""

import contextlib
import sqlite3

from example import Migration, ensure_version_table, run_pending


def test_migrations_apply_in_ascending_version_order_regardless_of_input_order() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        ensure_version_table(conn)  # => bookkeeping table set up
        migrations = [  # => deliberately shuffled input order
            Migration(version=2, sql="CREATE TABLE b(id INTEGER);"),
            Migration(version=1, sql="CREATE TABLE a(id INTEGER);"),
        ]
        order = run_pending(conn, migrations)  # => the runner sorts before applying
        assert order == [1, 2]  # => ascending, not input order


def test_already_applied_migrations_are_excluded_from_a_second_run() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        ensure_version_table(conn)
        migrations = [Migration(version=1, sql="CREATE TABLE a(id INTEGER);")]  # => one migration
        run_pending(conn, migrations)  # => first run applies it
        order = run_pending(conn, migrations)  # => second run -- nothing pending
        assert order == []  # => no migrations left to apply


# => Run: pytest -- Output: 2 passed
