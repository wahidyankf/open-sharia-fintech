# pyright: strict
"""Example 3: DB-API Parameterized Query."""

from __future__ import annotations

import os  # => reads connection settings from the environment (co-02)

import psycopg  # => the PEP 249 DB-API driver for Postgres

PG_DSN: str = os.environ.get(  # => a single DSN string -- host, port, db, user, password all in one place
    "PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example"
)  # => override PG_DSN in the environment to point at a different Postgres instance


def find_by_name(name: str) -> list[tuple[int, str]]:  # => `name` is untrusted input -- treat it as data, not code
    with psycopg.connect(PG_DSN, autocommit=True) as conn:  # => autocommit: no transaction to manage for this DDL+query
        conn.execute("DROP SCHEMA public CASCADE")  # => wipes EVERY table, including any left behind by a DIFFERENT example
        conn.execute("CREATE SCHEMA public")  # => a blank public schema -- fully isolated, run-in-any-order (self-contained)
        conn.execute("CREATE TABLE greeting(id SERIAL PRIMARY KEY, name TEXT NOT NULL)")  # => a minimal one-column table
        conn.execute("INSERT INTO greeting(name) VALUES (%s), (%s), (%s)", ["Ada", "Grace", "O'Brien"])  # => 3 placeholders, 3 bound values
        # => %s is psycopg's placeholder (co-05) -- the driver sends VALUES separately from the SQL text
        # => "O'Brien" contains a single quote; a naive f-string would have broken the SQL syntax right here
        cur = conn.execute(  # => the SAME %s placeholder style, this time in a WHERE clause
            "SELECT id, name FROM greeting WHERE name = %s ORDER BY id", (name,)
        )  # => `(name,)` -- a one-element tuple; the driver binds it to the single %s above
        rows: list[tuple[int, str]] = cur.fetchall()  # => materializes the matching rows as tuples
        return rows  # => hands the fully materialized list back to the caller


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    rows = find_by_name("O'Brien")  # => the exact value that would break naive string interpolation
    print(rows)  # => Output: [(3, "O'Brien")]
    assert rows == [(3, "O'Brien")]  # => the apostrophe round-tripped correctly -- no syntax error, no injection
    # => co-05: the SQL TEXT never changes between calls -- only the BOUND VALUE changes, which is the whole point
    # => psycopg sends the SQL and the parameters as SEPARATE messages -- the server never re-parses text with data spliced in
    print("ex-03 OK")  # => Output: ex-03 OK
