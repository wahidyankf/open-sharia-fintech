# pyright: strict
"""Example 64: The Same CRUD, ORM vs Raw SQL -- the ORM Is Shorter, Raw Is More Explicit."""

from __future__ import annotations

import os  # => reads connection settings from the environment

import psycopg  # => co-02: the raw DB-API driver, called directly -- no ORM in this half of the example
from sqlalchemy import Engine, create_engine, select, text  # => co-06: the ORM half of the same CRUD workload
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance
PG_DSN: str = os.environ.get("PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example")  # => a plain DB-API DSN, no dialect prefix


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-06: the SAME table both halves of this example read and write
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


def crud_orm(engine: Engine) -> str:  # => co-06 + co-25: Create/Read/Update/Delete through the ORM -- object-shaped
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        session.add(Customer(name="Ada"))  # => CREATE: add() registers the object, no SQL written by hand
        session.commit()  # => flushes the INSERT
        found = session.execute(select(Customer)).scalars().one()  # => READ: select(Customer) returns a mapped OBJECT
        found.name = "Ada Lovelace"  # => UPDATE: plain attribute assignment -- the unit of work tracks it as dirty
        session.commit()  # => flushes ONLY the changed column as an UPDATE
        session.delete(found)  # => DELETE: delete() marks the object for removal
        session.commit()  # => flushes the DELETE
    return "orm crud done in 6 lines of persistence code, zero SQL strings"  # => co-25: the ORM's leverage on CRUD


def crud_raw(dsn: str) -> str:  # => co-02 + co-25: the SAME four operations through raw parameterized SQL
    with psycopg.connect(dsn) as conn:  # => co-02: a plain DB-API connection, no ORM layer at all
        with conn.cursor() as cur:  # => a cursor executes statements and yields raw tuples, not objects
            cur.execute("INSERT INTO customer (name) VALUES (%s) RETURNING id", ("Ada",))  # => CREATE: explicit SQL, explicit params
            row = cur.fetchone()  # => co-02: manual row unpacking -- no automatic object mapping
            assert row is not None  # => narrows the type for pyright -- RETURNING always yields exactly one row here
            new_id = row[0]  # => co-02: index-based access -- you name the column position yourself, the ORM would not require this
            cur.execute("UPDATE customer SET name = %s WHERE id = %s", ("Ada Lovelace", new_id))  # => UPDATE: an explicit WHERE clause
            cur.execute("DELETE FROM customer WHERE id = %s", (new_id,))  # => DELETE: an explicit WHERE clause, same as UPDATE
        conn.commit()  # => co-02: raw DB-API requires an EXPLICIT commit -- no unit-of-work batching it for you
    return "raw crud done in 4 explicit statements, every WHERE and column written by hand"  # => co-25: raw SQL's explicitness


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, used only by the ORM half
    reset_schema(engine)  # => fresh, empty customer table before the ORM half runs

    orm_summary = crud_orm(engine)  # => co-25: runs the object-shaped CRUD path
    reset_schema(engine)  # => fresh, empty customer table again -- an IDENTICAL starting point for the raw half
    raw_summary = crud_raw(PG_DSN)  # => co-25: runs the explicit-SQL CRUD path

    # => co-25: BOTH halves ran identical logical operations against the SAME table -- the only difference is which
    # => layer wrote and tracked the SQL: SQLAlchemy's unit of work, or your own two hands
    print(f"orm: {orm_summary}")  # => Output: orm: orm crud done in 6 lines of persistence code, zero SQL strings
    print(f"raw: {raw_summary}")  # => Output: raw: raw crud done in 4 explicit statements, every WHERE and column written by hand
    assert "orm" in orm_summary  # => co-25: sanity check both summaries describe the path they claim to
    assert "raw" in raw_summary  # => co-25: sanity check both summaries describe the path they claim to
    # => co-25: for straightforward per-row CRUD, the ORM buys real leverage -- no hand-written INSERT/UPDATE/DELETE
    # => text, automatic change tracking, and a mapped OBJECT instead of an index-addressed tuple; raw SQL buys back
    # => full visibility into EVERY statement and WHERE clause, at the cost of writing and maintaining that SQL by hand
    print("ex-64 OK")  # => Output: ex-64 OK
