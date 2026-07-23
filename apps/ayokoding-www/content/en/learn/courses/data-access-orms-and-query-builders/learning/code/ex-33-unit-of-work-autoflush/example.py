# pyright: strict
"""Example 33: Unit of Work -- Autoflush Runs the Pending INSERT Before Your SELECT."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, create_engine, select, text  # => co-12: select() is what TRIGGERS autoflush below
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-12: the mapped class this example queries WHILE another instance is still pending
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
    with Session(engine) as session:  # => co-12: `autoflush=True` is the Session's DEFAULT -- not set explicitly here
        ada = Customer(name="Ada")  # => a transient object, about to become pending
        session.add(ada)  # => co-12: PENDING -- no INSERT sent yet, no commit() called either
        print(f"autoflush enabled: {session.autoflush}")  # => Output: autoflush enabled: True

        rows = session.execute(select(Customer)).scalars().all()  # => co-12: a plain SELECT, no commit() came before it
        # => this is the crux of autoflush: BEFORE running the SELECT against Postgres, the session flushed its own
        # => pending INSERT first -- otherwise the query would miss Ada entirely, contradicting the app's own in-memory
        # => view of the world (ada is clearly "there", the session just hadn't told Postgres about it yet)
        names = [row.name for row in rows]  # => reads the query's own result set
        print(f"names={names}")  # => Output: names=['Ada']
        assert names == ["Ada"]  # => co-12: the pending Ada WAS visible to the query -- autoflush ran first, automatically
        assert ada not in session.new  # => co-12: ada is no longer "new"/pending -- autoflush already promoted it to persistent

        session.commit()  # => co-17: commits the transaction the autoflush opened -- makes the write durable
    # => co-12: turning autoflush off (Session(engine, autoflush=False)) is rare and usually a mistake -- queries would
    # => then silently miss your own uncommitted writes, an easy source of "why doesn't my object show up" bugs
    print("ex-33 OK")  # => Output: ex-33 OK
