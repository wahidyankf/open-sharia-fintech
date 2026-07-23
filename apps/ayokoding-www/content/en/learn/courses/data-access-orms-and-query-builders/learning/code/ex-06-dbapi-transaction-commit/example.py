# pyright: strict
"""Example 6: DB-API Transaction Commit + Rollback."""

from __future__ import annotations

import os  # => reads connection settings from the environment (co-02)

import psycopg  # => the PEP 249 DB-API driver for Postgres

PG_DSN: str = os.environ.get(  # => a single DSN string -- host, port, db, user, password all in one place
    "PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example"
)  # => override PG_DSN in the environment to point at a different Postgres instance


def setup_table() -> None:  # => resets the shared table once, outside any of the transactions below
    with psycopg.connect(PG_DSN, autocommit=True) as conn:  # => autocommit: DDL needs no explicit commit
        conn.execute("DROP SCHEMA public CASCADE")  # => wipes EVERY table, including any left behind by a DIFFERENT example
        conn.execute("CREATE SCHEMA public")  # => a blank public schema -- fully isolated, run-in-any-order (self-contained)
        conn.execute("CREATE TABLE greeting(id SERIAL PRIMARY KEY, name TEXT NOT NULL)")  # => a minimal one-column table


def count_rows(conn: psycopg.Connection[tuple[int]]) -> int:  # => shared helper: how many rows exist right now
    row = conn.execute("SELECT COUNT(*) FROM greeting").fetchone()  # => a single aggregate row: (count,)
    assert row is not None  # => COUNT(*) always returns exactly one row
    return row[0]  # => unwraps the single integer count


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    setup_table()  # => empty `greeting` table to start
    # => two scenarios follow: one committed write, one rolled-back write -- only the FIRST should persist

    with psycopg.connect(PG_DSN) as conn:  # => NOT autocommit -- psycopg opens an implicit transaction (co-17) on first write
        conn.execute("INSERT INTO greeting(name) VALUES ('Ada')")  # => write happens INSIDE the open transaction
        conn.commit()  # => commit() (co-17) makes the write durable and visible to other connections
    with psycopg.connect(PG_DSN) as conn:  # => a fresh connection, to prove the commit is visible elsewhere
        after_commit = count_rows(conn)  # => reads the count from a DIFFERENT connection than the one that wrote
    print(f"after_commit={after_commit}")  # => Output: after_commit=1
    assert after_commit == 1  # => the committed row is durably visible

    with psycopg.connect(PG_DSN) as conn:  # => a second transaction, this one gets abandoned
        conn.execute("INSERT INTO greeting(name) VALUES ('Grace')")  # => write happens INSIDE this transaction too
        conn.rollback()  # => rollback() (co-17) discards every write since the transaction began
    with psycopg.connect(PG_DSN) as conn:  # => yet another fresh connection, to prove the rollback is durable
        after_rollback = count_rows(conn)  # => should still be 1 -- 'Grace' never actually landed
    print(f"after_rollback={after_rollback}")  # => Output: after_rollback=1
    assert after_rollback == 1  # => rollback() undid the second INSERT -- count did NOT become 2
    # => had we forgotten to call commit() or rollback() at all, closing the connection rolls back by default
    # => co-17: commit() and rollback() are the DB-API's two ways to end a transaction -- exactly one always applies
    print("ex-06 OK")  # => Output: ex-06 OK
