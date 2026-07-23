# pyright: strict
"""Example 44: begin_nested() -- a Savepoint That Rolls Back PART of a Transaction."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, create_engine, select, text  # => co-17: select() confirms exactly which rows survived
from sqlalchemy.exc import IntegrityError  # => co-17: the exact exception the inner savepoint's violation raises
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-17: the table this example writes to across an outer transaction and an inner savepoint
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column, UNIQUE below to force the savepoint's own write to fail


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
        conn.execute(text("CREATE TABLE customer (id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL)"))  # => raw DDL, adds UNIQUE


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer table with a UNIQUE name constraint

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        with session.begin():  # => co-17: the OUTER transaction -- this one commits at the very end, wrapping everything
            session.add(Customer(name="Ada"))  # => write #1, part of the OUTER transaction, survives regardless
            session.add(Customer(name="Grace"))  # => write #2, ALSO part of the OUTER transaction, survives regardless

            try:  # => an INNER savepoint, nested inside the still-open outer transaction
                with session.begin_nested():  # => co-17: begin_nested() opens a Postgres SAVEPOINT, not a whole new transaction
                    session.add(Customer(name="Ada"))  # => a DUPLICATE name -- violates UNIQUE, but only WITHIN this savepoint
            except IntegrityError:  # => co-17: begin_nested()'s `with` block rolls back to the SAVEPOINT, not the whole transaction
                print("inner savepoint rolled back")  # => Output: inner savepoint rolled back
                # => co-17: Ada and Grace from OUTSIDE the savepoint are untouched -- only the failed duplicate write is undone

    with Session(engine) as session:  # => a FRESH session, just to read back the final state
        names = sorted(session.execute(select(Customer.name)).scalars().all())  # => co-17: confirms exactly what survived
        print(f"names={names}")  # => Output: names=['Ada', 'Grace']
        assert names == ["Ada", "Grace"]  # => co-17: BOTH outer writes committed -- the inner savepoint's failure was ISOLATED
    # => co-17: this is the key difference from Example 43 -- there, the WHOLE transaction rolled back on failure;
    # => here, begin_nested() lets a caller attempt a risky write, catch its failure, and keep the surrounding
    # => transaction alive -- useful for "try this insert, fall back to something else" without losing prior work
    print("ex-44 OK")  # => Output: ex-44 OK
