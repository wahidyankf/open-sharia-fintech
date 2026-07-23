# pyright: strict
"""Example 29: Session Object States -- Transient, Pending, Persistent, Detached."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, create_engine, inspect, text  # => co-11: inspect() exposes an object's InstanceState
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.orm import InstanceState  # => the type inspect() returns for a mapped instance -- carries the phase flags


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-11: the mapped class this example tracks across all four states
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres, None before a flush
    name: Mapped[str]  # => a required TEXT column


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance

if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer table

    ada = Customer(name="Ada")  # => co-11: STATE 1 -- TRANSIENT. constructed but no Session has ever seen it
    state: InstanceState[Customer] = inspect(ada)  # => a handle onto the object's own InstanceState -- reads phase flags
    print(f"transient: {state.transient}")  # => Output: transient: True
    assert state.transient and not state.pending and not state.persistent and not state.detached  # => exactly one flag set

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        session.add(ada)  # => co-11: STATE 2 -- PENDING. the session knows about `ada`, but no INSERT has been sent yet
        print(f"pending: {state.pending}")  # => Output: pending: True
        assert state.pending and not state.transient and not state.persistent  # => the state object updates itself in place

        session.commit()  # => co-11 + co-12: STATE 3 -- PERSISTENT. flushes the INSERT, then commits -- now tracked in the
        # => Session's identity map, with a real primary key backing it
        print(f"persistent: {state.persistent}")  # => Output: persistent: True
        assert state.persistent and not state.pending  # => moved out of "pending" the moment the flush succeeded
        ada_id = ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below

    print(f"detached: {state.detached}")  # => Output: detached: True
    # => co-11: STATE 4 -- DETACHED. the `with` block above closed the session -- `ada` still exists in Python memory,
    # => still has its `id`, but is no longer tracked by ANY session's identity map or unit of work
    assert state.detached and not state.persistent  # => co-11: the full transient -> pending -> persistent -> detached arc
    print(f"final id={ada_id}")  # => Output: final id=1
    # => co-11: these four states are exactly the four SQLAlchemy uses to describe an object's persistence lifecycle
    print("ex-29 OK")  # => Output: ex-29 OK
