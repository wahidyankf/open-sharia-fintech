# pyright: strict
"""Example 32: Unit of Work -- Dirty Tracking Writes Only Changed Columns."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, create_engine, event, select, text  # => co-12: event captures the emitted UPDATE's own SQL
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-12: three columns, only ONE of which this example mutates
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column -- this one gets mutated below
    email: Mapped[str]  # => a required TEXT column -- this one is NEVER touched after the insert
    country: Mapped[str]  # => a required TEXT column -- this one is NEVER touched after the insert either


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer table
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Customer(name="Ada", email="ada@example.com", country="UK")  # => three columns, all set at insert time
        session.add(ada)  # => registers `ada` as pending
        session.commit()  # => flushes the INSERT, assigns ada.id
        ada_id = ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below

    statements: list[str] = []  # => captures the RAW SQL of every statement, for inspecting exactly which columns appear

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        statements.append(statement)  # => records the RAW SQL text SQLAlchemy is about to send to Postgres

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`

    with Session(engine) as session:  # => a FRESH session -- reloads Ada, then mutates ONLY her name
        loaded = session.execute(select(Customer).where(Customer.id == ada_id)).scalar_one()  # => reload by PK
        loaded.name = "Ada Lovelace"  # => co-12: mutating ONE attribute -- the session's dirty-tracking notices THIS one
        # => `loaded.email` and `loaded.country` are untouched -- the unit of work knows the difference between "loaded"
        # => and "changed", because it snapshots every attribute at load time and diffs against that snapshot on flush
        session.commit()  # => flushes ONLY the dirty column(s), then commits

    update_statements = [s for s in statements if s.strip().upper().startswith("UPDATE")]  # => filters to the one UPDATE
    print(update_statements)  # => Output: ['UPDATE customer SET name=%(name)s::VARCHAR WHERE customer.id = %(customer_id)s::INTEGER']
    assert len(update_statements) == 1  # => exactly one UPDATE was emitted
    assert "email" not in update_statements[0] and "country" not in update_statements[0]  # => co-12: the UNCHANGED columns
    # => never appear in the SET clause at all -- SQLAlchemy does not blindly re-write every column on every save
    # => contrast with a hand-rolled "UPDATE customer SET name=%s, email=%s, country=%s" -- Active Record libraries that
    # => lack dirty tracking often do exactly that, re-sending every column whether it changed or not
    print("ex-32 OK")  # => Output: ex-32 OK
