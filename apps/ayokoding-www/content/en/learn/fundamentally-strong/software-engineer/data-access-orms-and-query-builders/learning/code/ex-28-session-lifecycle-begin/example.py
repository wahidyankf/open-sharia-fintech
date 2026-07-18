# pyright: strict
"""Example 28: Session Lifecycle -- Open, Add, Commit, Close."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, create_engine, text  # => co-11: the engine a Session opens connections FROM
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-11: the mapped class this example walks through a full session lifecycle with
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => co-11: a connection FACTORY -- a Session borrows a connection from it as needed
    reset_schema(engine)  # => fresh, empty customer table

    session = Session(engine)  # => co-11: STAGE 1 -- OPEN. no connection is actually borrowed yet, this is lazy
    print(f"is_active before any work: {session.is_active}")  # => Output: is_active before any work: True
    # => co-11: `is_active` is True the whole time the session is NOT inside a failed transaction -- it does not mean
    # => "has a live database connection" -- SQLAlchemy borrows/returns the underlying connection lazily, per statement

    ada = Customer(name="Ada")  # => co-11: STAGE 2 -- ADD. constructs a transient object, not yet known to the session
    session.add(ada)  # => co-11: registers `ada` as PENDING -- still no SQL sent to Postgres
    print(f"ada in session.new: {ada in session.new}")  # => Output: ada in session.new: True
    # => co-11: `session.new` is the set of pending-insert objects -- this is the session's own bookkeeping, visible
    # => before any flush happens

    session.commit()  # => co-11 + co-17: STAGE 3 -- COMMIT. flushes the pending INSERT, then commits the transaction
    print(f"ada in session.new after commit: {ada in session.new}")  # => Output: ada in session.new after commit: False
    # => co-17: after commit(), `ada` is no longer pending -- it is now a PERSISTENT object, tracked in the identity map
    assigned_id = ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below

    session.close()  # => co-11: STAGE 4 -- CLOSE. releases the borrowed connection back to the engine's pool
    print(f"is_active after close: {session.is_active}")  # => Output: is_active after close: True
    # => co-11: `is_active` still reads True -- close() ends the session's transactional scope and expires its objects,
    # => but does not itself flip is_active to False; a NEW session must be opened to do any further work with `ada`
    print(f"assigned_id={assigned_id}")  # => Output: assigned_id=1
    assert assigned_id == 1  # => co-11: the full open -> add -> commit -> close arc produced exactly one persisted row
    print("ex-28 OK")  # => Output: ex-28 OK
