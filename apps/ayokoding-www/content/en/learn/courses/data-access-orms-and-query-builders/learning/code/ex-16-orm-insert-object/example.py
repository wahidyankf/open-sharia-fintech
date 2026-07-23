# pyright: strict
"""Example 16: ORM Insert -- Add an Object, Commit."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, create_engine, text  # => Engine: the typed handle every helper below takes
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column  # => co-06 + co-17: object graph + session

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-06: the mapped class this example inserts an instance of
    __tablename__ = "customer"  # => the physical table name this class maps to
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres -- never set by hand below
    name: Mapped[str]  # => a required TEXT column


def reset_schema(engine: Engine) -> None:  # => shared reset helper, same "wipe the whole schema" pattern as before
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer table

    ada = Customer(name="Ada")  # => co-06: an ordinary Python object -- NOT yet a row in Postgres
    print(f"before commit: id={ada.id}")  # => Output: before commit: id=None
    # => co-17: `ada` is TRANSIENT -- it exists only in Python memory, with no primary key assigned yet
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        session.add(ada)  # => registers `ada` as PENDING -- still no INSERT has run yet
        session.commit()  # => co-17: flushes the pending INSERT, then commits the transaction in one call
        print(f"after commit: id={ada.id}")  # => Output: after commit: id=1
    # => co-17: Postgres assigned the primary key DURING flush -- commit() populated `ada.id` as a side effect
    assert ada.id == 1  # => confirms the SAME Python object now carries the database-assigned id
    # => co-06 + co-17: `session.add()` plus `session.commit()` is the ORM's entire "persist this" vocabulary
    print("ex-16 OK")  # => Output: ex-16 OK
