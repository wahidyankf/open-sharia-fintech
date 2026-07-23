# pyright: strict
"""Example 18: ORM Update -- Mutate + Commit."""

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


class Customer(Base):  # => co-06 + co-12: the mapped class this example mutates in place
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => the column this example changes


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer table
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Customer(name="Ada")  # => the object this example will load, mutate, and re-save
        session.add(ada)  # => registers `ada` as pending
        session.commit()  # => flushes the INSERT, assigns ada.id
        ada_id = ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below

    statements: list[str] = []  # => co-12: every SQL statement the ORM emits, captured for verification below

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (co-12's plumbing)
        statements.append(statement)  # => records the RAW SQL text SQLAlchemy is about to send to Postgres
        # => this same "before_cursor_execute" hook is how Example 42 later counts N+1 queries too

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`
    # => from here on, EVERY statement this engine runs gets appended to `statements`, seed writes included

    with Session(engine) as session:  # => a FRESH session -- loads Ada, mutates her, and commits the change
        loaded = session.execute(select(Customer).where(Customer.id == ada_id)).scalar_one()  # => reload by PK
        loaded.name = "Ada Lovelace"  # => co-12: mutating a PERSISTENT object -- no explicit UPDATE statement written
        session.commit()  # => co-12: the Session detects the change and flushes exactly one UPDATE

    update_statements = [s for s in statements if s.strip().upper().startswith("UPDATE")]  # => filters the captured SQL
    print(update_statements)  # => Output: ['UPDATE customer SET name=%(name)s::VARCHAR WHERE customer.id = %(customer_id)s::INTEGER']
    assert len(update_statements) == 1  # => confirms exactly one UPDATE was emitted -- the mutation, and only that
    # => not two, not zero -- the Session batches the single change into a single statement (foreshadows co-12's dirty tracking)
    assert "customer" in update_statements[0].lower()  # => confirms it targeted the customer table
    assert "name" in update_statements[0]  # => confirms the SET clause targeted exactly the column that changed
    # => co-12: this is the Session's unit-of-work in action -- Python attribute assignment BECOMES a SQL UPDATE
    # => contrast with Core (Example 13): there, you write conn.execute(table.update()...) explicitly -- here, you don't
    print("ex-18 OK")  # => Output: ex-18 OK
