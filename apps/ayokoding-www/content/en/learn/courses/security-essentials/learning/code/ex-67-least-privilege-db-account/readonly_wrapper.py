# learning/code/ex-67-least-privilege-db-account/readonly_wrapper.py
"""Example 67: a real app-layer SELECT-only wrapper -- an HONEST stand-in for a real DB-native read-only role (co-16, co-03)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the wrapper logic itself

import sqlite3  # => co-16: stdlib DB driver -- SQLite itself has NO GRANT/role system, hence this wrapper exists

# => co-16: HONEST LIMITATION -- SQLite has no native GRANT/role system at all. In a real
# => Postgres deployment, the equivalent, DB-ENFORCED control is:
# =>   CREATE ROLE readonly_app LOGIN PASSWORD '...';
# =>   GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_app;
# => and in real MySQL:
# =>   CREATE USER 'readonly_app'@'%' IDENTIFIED BY '...';
# =>   GRANT SELECT ON dbname.* TO 'readonly_app'@'%';
# => Both of THOSE are enforced by the database server itself, independent of the application's
# => code -- a compromised app process literally cannot issue a DROP/DELETE no matter what SQL
# => text it builds. The wrapper below is an APPLICATION-LAYER substitute for this example's
# => sandbox (SQLite), not a claim that it is equally strong -- a bug in this wrapper's own code
# => would bypass it, whereas a real GRANT is enforced entirely outside the application process.


class PermissionError_(
    PermissionError
):  # => co-16: a real, named exception type this wrapper raises
    """Raised when a statement other than a single SELECT reaches the read-only wrapper."""


class ReadOnlyConnection:  # => co-16: wraps a REAL sqlite3.Connection -- every call is a REAL SQLite operation underneath
    def __init__(
        self, real_connection: sqlite3.Connection
    ) -> None:  # => co-16: takes an ALREADY-OPEN real connection
        self._conn = real_connection  # => co-16: the REAL underlying connection -- never exposed directly to callers

    def _assert_single_select(
        self, sql: str
    ) -> None:  # => co-16: the ONE real check both entry points below share
        statements = [
            s.strip() for s in sql.split(";") if s.strip()
        ]  # => co-16: splits on ';' -- catches STACKED queries
        if (
            len(statements) != 1
        ):  # => co-16: more than one real statement means a stacked-query attempt, full stop
            raise PermissionError_(
                f"read-only role rejects multi-statement input: {sql!r}"
            )  # => co-16: real, hard reject
        if (
            not statements[0].upper().startswith("SELECT")
        ):  # => co-16: the REAL, single allowed statement shape
            raise PermissionError_(
                f"read-only role rejects non-SELECT statement: {sql!r}"
            )  # => co-16: real, hard reject

    def execute(
        self, sql: str, params: tuple[object, ...] = ()
    ) -> sqlite3.Cursor:  # => co-16: guarded single-statement path
        self._assert_single_select(
            sql
        )  # => co-16: real validation BEFORE the real driver ever sees this SQL text
        return self._conn.execute(
            sql, params
        )  # => co-16: ONLY reached for a real, single, genuine SELECT statement

    def executescript(
        self, sql: str
    ) -> sqlite3.Cursor:  # => co-16: guarded multi-statement path -- SAME real check
        # => co-16: real sqlite3.Cursor.execute() ALREADY refuses multi-statement input on its own
        # => (raises ProgrammingError) -- executescript() is the real driver method that does NOT,
        # => which is exactly why a naive app using executescript() for "convenience" is dangerous
        self._assert_single_select(
            sql
        )  # => co-16: the SAME real guard -- a stacked payload is rejected before it runs
        return self._conn.executescript(
            sql
        )  # => co-16: ONLY reached for a real, single, genuine SELECT statement
