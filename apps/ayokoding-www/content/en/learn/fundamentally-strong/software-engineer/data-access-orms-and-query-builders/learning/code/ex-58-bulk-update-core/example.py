# pyright: strict
"""Example 58: Core update() -- ONE Set-Based UPDATE for Many Rows, Not a Per-Object Loop."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, create_engine, event, select, text, update  # => co-23: update() builds ONE set-based statement
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Product(Base):  # => co-23: the table this example applies a blanket price change to
    __tablename__ = "product"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    price_cents: Mapped[int]  # => cents, not a float, to avoid rounding drift (co-05 spirit)


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Product's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE product from Product's Mapped[] fields


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty product table
    n_rows = 100  # => co-23: enough rows to make the per-statement round-trip count meaningfully visible below
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        for i in range(n_rows):  # => seeds 100 products, all at the SAME starting price
            session.add(Product(price_cents=1000))  # => every row starts at $10.00
        session.commit()  # => flushes all 100 INSERTs

    update_statements: list[str] = []  # => every UPDATE the ORM emits during the bulk change, captured for verification

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("UPDATE"):  # => this example only cares about the bulk write
            update_statements.append(statement)  # => records the STATEMENT TEXT itself, not just a count

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`

    with Session(engine) as session:  # => a FRESH session -- nothing loaded, so no per-object change tracking happens
        stmt = update(Product).values(price_cents=Product.price_cents + 100)  # => co-23: a SET-BASED expression, computed IN Postgres
        # => `Product.price_cents + 100` compiles to `price_cents = price_cents + 100` -- Postgres reads AND writes each row
        # => in ONE pass, without SQLAlchemy ever pulling the CURRENT value back into Python first
        session.execute(stmt)  # => co-23: ONE UPDATE statement, no WHERE clause -- applies to EVERY row in the table
        session.commit()  # => co-23: durably raises every product's price by exactly 100 cents, in a single round trip

    with Session(engine) as session:  # => a fresh session, just to read back the final prices
        prices = sorted(session.execute(select(Product.price_cents)).scalars().all())  # => co-23: confirms the blanket change
    print(f"unique prices after update: {set(prices)}")  # => Output: unique prices after update: {1100}
    print(f"UPDATE statements emitted: {len(update_statements)}")  # => Output: UPDATE statements emitted: 1
    assert set(prices) == {1100}  # => co-23: EVERY row moved from 1000 to 1100 cents -- one consistent value across all 100
    assert len(update_statements) == 1  # => co-23: ONE statement, not 100 -- contrast this with a per-object ORM loop
    # => co-23: a per-object loop (`for p in session.query(Product): p.price_cents += 100`) would first SELECT every
    # => row into Python objects, mutate each one, then flush 100 separate UPDATEs -- Core's update() skips loading
    # => rows into Python entirely and lets Postgres compute the new value directly, in ONE set-based statement
    print("ex-58 OK")  # => Output: ex-58 OK
