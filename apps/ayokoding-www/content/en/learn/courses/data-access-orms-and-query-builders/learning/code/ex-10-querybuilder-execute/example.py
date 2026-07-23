# pyright: strict
"""Example 10: Query Builder -- Execute a Built Query."""

from __future__ import annotations

import os  # => reads connection settings from the environment (co-02)
from typing import LiteralString, cast  # => acknowledges a builder-rendered string is safe to execute

import psycopg  # => co-03: the builder only BUILDS -- the DB-API still does the actual talking to Postgres
from pypika import Query, Table

PG_DSN: str = os.environ.get(  # => a single DSN string -- host, port, db, user, password all in one place
    "PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example"
)  # => override PG_DSN in the environment to point at a different Postgres instance
product = Table("product")  # => the table this example builds a query against


def seed() -> None:  # => resets and seeds the `product` table this example reads from
    with psycopg.connect(PG_DSN, autocommit=True) as conn:  # => autocommit: no transaction to manage for this DDL+write
        conn.execute("DROP SCHEMA public CASCADE")  # => wipes EVERY table, including any left behind by a DIFFERENT example
        conn.execute("CREATE SCHEMA public")  # => a blank public schema -- fully isolated, run-in-any-order (self-contained)
        conn.execute("CREATE TABLE product(id SERIAL PRIMARY KEY, name TEXT NOT NULL, price NUMERIC(10,2) NOT NULL)")  # => NUMERIC for money
        conn.execute("INSERT INTO product(name, price) VALUES ('Widget', 9.99), ('Gadget', 19.99)")  # => two seed rows
        # => Widget is cheap, Gadget is not -- deliberately straddling the $10 filter the query below applies


def run_built_query() -> list[tuple[int, str]]:  # => returns raw tuples -- the DB-API's native shape, same as Tier 1
    query = Query.from_(product).select(product.id, product.name).where(product.price > 10)  # => co-03: built, not typed
    # => `product.price > 10` is a Field COMPARISON object -- PyPika renders it, it does not run it
    sql_text = cast(LiteralString, str(query))  # => render the tree, then vouch it is safe to run
    with psycopg.connect(PG_DSN) as conn:  # => the SAME connect/execute/fetchall cycle Example 2 used directly
        return conn.execute(sql_text).fetchall()  # => the DB-API executes PyPika's rendered output, unchanged
        # => this is co-03's whole shape: BUILD with PyPika, then EXECUTE with the DB-API -- two separate concerns


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    seed()  # => two products: Widget ($9.99) and Gadget ($19.99)
    rows = run_built_query()  # => builds a "price > 10" filter, then actually runs it against Postgres
    print(rows)  # => Output: [(2, 'Gadget')]
    assert rows == [(2, "Gadget")]  # => only Gadget clears the $10 threshold -- Widget was correctly filtered out
    # => co-03's whole point made concrete: the builder produces TEXT, and the DB-API is what actually runs it
    print("ex-10 OK")  # => Output: ex-10 OK
