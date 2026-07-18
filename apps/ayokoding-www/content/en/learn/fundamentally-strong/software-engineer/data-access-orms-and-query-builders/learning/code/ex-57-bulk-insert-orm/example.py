# pyright: strict
"""Example 57: Bulk Insert -- One Statement for Many Rows, Instead of Many round trips."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, create_engine, event, insert, select, text  # => co-23: insert() builds ONE bulk statement
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-23: the table this example writes MANY rows into with a single round trip
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer table
    n_rows = 100  # => co-23: enough rows to make the per-statement round-trip count meaningfully visible below

    insert_statements: list[str] = []  # => every INSERT the ORM emits during the bulk write, captured for verification

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("INSERT"):  # => this example only cares about write traffic
            insert_statements.append(statement)  # => records the STATEMENT TEXT itself, not just a count

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`

    with Session(engine) as session:  # => co-23: Core's insert() runs THROUGH a Session's own connection just fine
        rows = [{"name": f"Customer{i}"} for i in range(n_rows)]  # => co-23: plain dicts, ONE per row -- no ORM objects at all
        session.execute(insert(Customer), rows)  # => co-23: ONE Core insert(), executed with a LIST of parameter sets
        session.commit()  # => co-23: psycopg batches these into `executemany`-style network traffic, not N round trips

    with Session(engine) as session:  # => a FRESH session, just to read back the final row count
        count = session.execute(select(Customer)).scalars().all()  # => confirms every row actually landed

    print(f"rows inserted: {len(count)}")  # => Output: rows inserted: 100
    print(f"INSERT statements emitted: {len(insert_statements)}")  # => Output: INSERT statements emitted: 1
    assert len(count) == n_rows  # => co-23: all 100 rows are really in Postgres
    assert len(insert_statements) == 1  # => co-23: ONE statement, not 100 -- contrast this with a per-object ORM loop
    # => co-23: `session.add()` in a loop, called 100 times, would issue 100 separate INSERTs during flush (or one
    # => per-object round trip in the worst case); `insert(Customer)` executed with a LIST of dicts collapses that
    # => into ONE statement the driver sends as a single batched operation -- the ORM's identity map and change
    # => tracking never get involved, because these rows never become tracked Python OBJECTS at all -- pure throughput
    print("ex-57 OK")  # => Output: ex-57 OK
