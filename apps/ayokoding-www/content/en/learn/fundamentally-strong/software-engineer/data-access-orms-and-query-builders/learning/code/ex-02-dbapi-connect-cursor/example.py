# pyright: strict
"""Example 2: DB-API Connect + Cursor."""

from __future__ import annotations

import os  # => reads connection settings from the environment (co-02)

import psycopg  # => the PEP 249 DB-API driver for Postgres

PG_DSN: str = os.environ.get(  # => a single DSN string -- host, port, db, user, password all in one place
    "PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example"
)  # => override PG_DSN in the environment to point at a different Postgres instance


def connect_and_query() -> list[tuple[int, str]]:  # => returns raw (id, name) tuples -- the DB-API's native shape
    # => connect() (co-02) opens a Connection -- one TCP round-trip to the server, nothing queried yet
    with psycopg.connect(PG_DSN, autocommit=True) as conn:  # => autocommit: no transaction to manage for this DDL+query
        cur: psycopg.Cursor[tuple[int, str]] = conn.cursor()  # => a Cursor executes statements against conn
        cur.execute("DROP SCHEMA public CASCADE")  # => wipes EVERY table, including any left behind by a DIFFERENT example
        cur.execute("CREATE SCHEMA public")  # => a blank public schema -- fully isolated, run-in-any-order (self-contained)
        cur.execute("CREATE TABLE greeting(id SERIAL PRIMARY KEY, text TEXT NOT NULL)")  # => a minimal one-column table
        cur.execute("INSERT INTO greeting(text) VALUES ('hello'), ('world')")  # => two rows, ids auto-assigned 1 and 2
        cur.execute("SELECT id, text FROM greeting ORDER BY id")  # => sends the SQL text -- nothing fetched into Python yet
        rows: list[tuple[int, str]] = cur.fetchall()  # => fetchall() pulls every remaining row as a list of tuples
        return rows  # => hands the fully materialized list back to the caller


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    rows = connect_and_query()  # => runs the full connect -> cursor -> execute -> fetchall cycle once
    # => everything above is the PEP 249 DB-API contract (co-02) -- every higher tier in this topic sits on top of it
    for row in rows:  # => iterates the (id, text) tuples one at a time
        print(row)  # => Output: (1, 'hello') then (2, 'world')
    assert rows == [(1, "hello"), (2, "world")]  # => confirms both rows round-tripped in insertion order
    # => no query builder, no ORM -- just connect(), cursor(), execute(), fetchall(): the DB-API's whole surface
    print("ex-02 OK")  # => Output: ex-02 OK
