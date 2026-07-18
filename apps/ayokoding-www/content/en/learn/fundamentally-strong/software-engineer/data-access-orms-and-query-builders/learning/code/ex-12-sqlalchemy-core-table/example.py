# pyright: strict
"""Example 12: SQLAlchemy Core -- Table + MetaData."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, inspect, text  # => co-04: Core's own builder

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance

metadata = MetaData()  # => co-04: a MetaData registry -- every Core Table below registers itself here
# => a Core Table describes a schema; it is not itself a query -- co-03's "compose, don't concatenate" idea extends here
customer = Table(  # => co-03 + co-04: SQLAlchemy Core's OWN query-builder Table, not PyPika's
    "customer",  # => the physical table name
    metadata,  # => registers this Table under `metadata` -- required as Core's second positional argument
    Column("id", Integer, primary_key=True),  # => a Core Column, typed via SQLAlchemy's own type objects
    Column("name", String, nullable=False),  # => String maps to Postgres TEXT/VARCHAR; nullable=False -> NOT NULL
)


def create_and_inspect() -> list[str]:  # => returns the column names Postgres actually stored, for verification
    engine = create_engine(SQLA_URL)  # => a Core engine -- no ORM classes involved anywhere in this example
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table, not just this example's own
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema -- fully isolated from other examples
    metadata.create_all(engine)  # => co-04: Core ISSUES the CREATE TABLE DDL from the Table object above
    inspector = inspect(engine)  # => Inspector reads the database's OWN catalog, independent of our Table object
    return [col["name"] for col in inspector.get_columns("customer")]  # => what Postgres actually has, not what we assumed
    # => Inspector.get_columns() round-trips through Postgres' information_schema -- it cannot be fooled by a stale Table


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    columns = create_and_inspect()  # => creates the table, then reads its columns back from Postgres itself
    print(columns)  # => Output: ['id', 'name']
    assert columns == ["id", "name"]  # => confirms the physical schema matches the Core Table definition exactly
    # => co-04: this Table is METADATA -- a Python description of a schema -- not a query by itself
    # => Example 14 reuses this SAME idea, but attaches Python behavior to the mapped class -- that's the ORM's addition
    print("ex-12 OK")  # => Output: ex-12 OK
