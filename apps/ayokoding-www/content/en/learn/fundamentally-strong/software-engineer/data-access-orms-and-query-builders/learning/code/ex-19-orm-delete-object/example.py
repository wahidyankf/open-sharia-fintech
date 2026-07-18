# pyright: strict
"""Example 19: ORM Delete -- session.delete() + Commit."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, create_engine, event, select, text  # => event: hooks into the engine's own SQL emission
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-06: the mapped class this example deletes an instance of
    __tablename__ = "customer"
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
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Customer(name="Ada")  # => the object this example will load, then delete
        session.add(ada)  # => registers `ada` as pending
        session.commit()  # => flushes the INSERT, assigns ada.id
        ada_id = ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below

    statements: list[str] = []  # => every SQL statement the ORM emits, captured for verification below

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        statements.append(statement)  # => records the RAW SQL text SQLAlchemy is about to send to Postgres

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`
    # => from here on, EVERY statement this engine runs gets appended to `statements`
    # => same capture technique as Example 18 -- reused here to verify DELETE instead of UPDATE

    with Session(engine) as session:  # => a FRESH session -- loads Ada, then deletes her
        loaded = session.execute(select(Customer).where(Customer.id == ada_id)).scalar_one()  # => reload by PK
        session.delete(loaded)  # => co-06: marks `loaded` for deletion -- no DELETE statement written yet
        session.commit()  # => flushes the pending delete as one DELETE statement, then commits
        # => co-12: same unit-of-work pattern as the UPDATE in Example 18 -- the change waits for flush, not for the call site

    delete_statements = [s for s in statements if s.strip().upper().startswith("DELETE")]  # => filters the captured SQL
    print(delete_statements)  # => Output: ['DELETE FROM customer WHERE customer.id = %(id)s::INTEGER']
    assert len(delete_statements) == 1  # => confirms exactly one DELETE was emitted for the one deleted object
    # => not a `DROP TABLE`, not a bulk `DELETE FROM customer` -- one row, targeted by its primary key

    with Session(engine) as session:  # => a THIRD session -- confirms the row is actually gone from Postgres
        remaining = session.execute(select(Customer)).scalars().all()  # => everything left in the customer table
    print(remaining)  # => Output: []
    assert remaining == []  # => co-06: the row is gone -- session.delete() + commit() is symmetrical with add() + commit()
    # => co-06's full CRUD arc across Examples 16-19: add() -> INSERT, mutate -> UPDATE, delete() -> DELETE
    print("ex-19 OK")  # => Output: ex-19 OK
