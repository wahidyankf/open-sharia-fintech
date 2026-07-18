# pyright: strict
"""Example 5: DB-API executemany -- Batch Insert."""

from __future__ import annotations

import os  # => reads connection settings from the environment (co-02)

import psycopg  # => the PEP 249 DB-API driver for Postgres

PG_DSN: str = os.environ.get(  # => a single DSN string -- host, port, db, user, password all in one place
    "PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example"
)  # => override PG_DSN in the environment to point at a different Postgres instance


def batch_insert(names: list[str]) -> int:  # => returns the row COUNT actually inserted, for verification
    with psycopg.connect(PG_DSN, autocommit=True) as conn:  # => autocommit: no transaction to manage for this DDL+bulk-write
        conn.execute("DROP SCHEMA public CASCADE")  # => wipes EVERY table, including any left behind by a DIFFERENT example
        conn.execute("CREATE SCHEMA public")  # => a blank public schema -- fully isolated, run-in-any-order (self-contained)
        conn.execute("CREATE TABLE greeting(id SERIAL PRIMARY KEY, name TEXT NOT NULL)")  # => a minimal one-column table
        params_seq: list[tuple[str]] = [(name,) for name in names]  # => one 1-tuple of bound params PER row to insert
        # => executemany() (co-02) runs the SAME parameterized statement once per tuple in params_seq
        with conn.cursor() as cur:  # => a fresh cursor scoped to this batch write
            cur.executemany("INSERT INTO greeting(name) VALUES (%s)", params_seq)  # => one round-trip PLAN, many bound executions
            return cur.rowcount  # => rowcount after executemany() reports the LAST statement's count under psycopg,
            # => so verification below re-queries COUNT(*) instead of trusting this value across drivers


def count_rows() -> int:  # => re-queries the table directly -- the portable way to verify a bulk write landed
    with psycopg.connect(PG_DSN, autocommit=True) as conn:
        row = conn.execute("SELECT COUNT(*) FROM greeting").fetchone()  # => a single aggregate row: (count,)
        assert row is not None  # => the table exists (created above) -- COUNT(*) always returns exactly one row
        return int(row[0])  # => unwraps the single integer count from that one-column row


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    names = ["Ada", "Grace", "Alan", "Katherine"]  # => 4 names -- the batch this example inserts in one call
    batch_insert(names)  # => sends 4 bound executions of the SAME INSERT statement in one executemany() call
    total = count_rows()  # => independently confirms how many rows actually landed
    print(f"total={total}")  # => Output: total=4
    assert total == len(names)  # => every name in the batch produced exactly one row -- none silently dropped
    # => contrast with 4 separate execute() calls: same end result here, but 4 round-trips instead of 1
    # => co-02: executemany() is still the raw DB-API -- no query builder, no ORM batching machinery involved
    print("ex-05 OK")  # => Output: ex-05 OK
