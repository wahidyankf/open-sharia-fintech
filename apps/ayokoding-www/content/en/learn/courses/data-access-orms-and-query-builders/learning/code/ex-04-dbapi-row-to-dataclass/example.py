# pyright: strict
"""Example 4: DB-API Row -> Typed Dataclass."""

from __future__ import annotations

import os  # => reads connection settings from the environment (co-02)
from dataclasses import dataclass  # => a typed, immutable shape for each row -- better than a bare tuple

import psycopg
from psycopg.rows import class_row  # => a psycopg row_factory that builds a chosen class from each row

PG_DSN: str = os.environ.get(  # => a single DSN string -- host, port, db, user, password all in one place
    "PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example"
)  # => override PG_DSN in the environment to point at a different Postgres instance


@dataclass(frozen=True)  # => frozen: a fetched row should not silently mutate after the fact
class Greeting:  # => co-02: the typed shape raw DB-API rows get promoted into
    id: int  # => matches the `id` column's SQL type (SERIAL -> Python int)
    text: str  # => matches the `text` column's SQL type (TEXT -> Python str)


def fetch_greetings() -> list[Greeting]:  # => the return type IS the dataclass -- no bare tuples leak out
    with psycopg.connect(PG_DSN, autocommit=True) as conn:  # => autocommit: no transaction to manage for this DDL+query
        conn.execute("DROP SCHEMA public CASCADE")  # => wipes EVERY table, including any left behind by a DIFFERENT example
        conn.execute("CREATE SCHEMA public")  # => a blank public schema -- fully isolated, run-in-any-order (self-contained)
        conn.execute("CREATE TABLE greeting(id SERIAL PRIMARY KEY, text TEXT NOT NULL)")  # => matches Greeting's fields
        conn.execute("INSERT INTO greeting(text) VALUES ('hello'), ('world')")  # => two rows, ids 1 and 2
        # => class_row() is a row_factory: it swaps the DEFAULT tuple-per-row behavior for one typed instance per row
        with conn.cursor(row_factory=class_row(Greeting)) as cur:  # => every fetched row becomes a Greeting, not a tuple
            cur.execute("SELECT id, text FROM greeting ORDER BY id")  # => column NAMES must match Greeting's field names
            return cur.fetchall()  # => already typed as list[Greeting] -- no manual unpacking needed
            # => this promotion is opt-in per cursor -- Example 2's default cursor still returns plain tuples


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    greetings = fetch_greetings()  # => runs the full connect -> class_row -> fetchall cycle once
    for g in greetings:  # => iterates typed Greeting objects, not raw tuples
        print(f"{g.id}: {g.text}")  # => Output: 1: hello then 2: world
        # => `g.id`/`g.text` are named, typed attribute accesses -- not `g[0]`/`g[1]` index lookups
    assert greetings == [Greeting(1, "hello"), Greeting(2, "world")]  # => dataclass equality compares field-by-field
    assert isinstance(greetings[0], Greeting)  # => confirms the row_factory built the CLASS, not a plain tuple
    # => this is the seam co-02's PEP 249 rows and every later tier's typed objects (co-06) both grow from
    print("ex-04 OK")  # => Output: ex-04 OK
