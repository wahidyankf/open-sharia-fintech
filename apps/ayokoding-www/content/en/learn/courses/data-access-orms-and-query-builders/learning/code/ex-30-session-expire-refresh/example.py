# pyright: strict
"""Example 30: session.expire() + refresh() -- Forcing a Reload From Postgres."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, create_engine, text  # => co-11: the engine a Session opens connections FROM
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-11: the mapped class this example expires and refreshes
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column, mutated OUTSIDE the ORM later in this example


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer table
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Customer(name="Ada")  # => the row this example mutates OUTSIDE the ORM's own knowledge
        session.add(ada)  # => registers `ada` as pending
        session.commit()  # => flushes the INSERT, assigns ada.id
        ada_id = ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below

        with engine.begin() as raw_conn:  # => co-11: a SEPARATE raw connection -- bypasses this session's ORM entirely
            raw_conn.execute(text("UPDATE customer SET name = 'Ada Lovelace' WHERE id = :id"), {"id": ada_id})
            # => this UPDATE happens BEHIND the session's back -- `ada.name` in Python memory is now stale

        print(f"before refresh: {ada.name}")  # => Output: before refresh: Ada
        # => co-11: the session has NO reason to know the row changed -- it still trusts its own in-memory copy

        session.expire(ada)  # => co-11: marks `ada`'s attributes as stale -- does NOT reload them yet, just discards them
        # => expire() alone is lazy: the NEXT attribute access would trigger a reload -- refresh() below makes it eager
        session.refresh(ada)  # => co-11: forces an immediate reload -- issues a fresh SELECT for this object's PK
        print(f"after refresh: {ada.name}")  # => Output: after refresh: Ada Lovelace
        assert ada.name == "Ada Lovelace"  # => co-11: expire() + refresh() is the ORM's explicit "trust the database now"
        # => escape hatch -- without it, an object silently diverges from a row another process (or connection) changed
        # => Example 33 shows the OTHER trigger for a reload: querying, not calling refresh() by hand
    print("ex-30 OK")  # => Output: ex-30 OK
