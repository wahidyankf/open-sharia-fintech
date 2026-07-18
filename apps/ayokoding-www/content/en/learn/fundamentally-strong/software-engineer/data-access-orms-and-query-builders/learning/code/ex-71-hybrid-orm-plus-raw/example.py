# pyright: strict
"""Example 71: ORM for CRUD + a Raw-SQL Escape Hatch -- Both in One App, One Session."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from typing import Any, cast  # => cast() narrows session.execute()'s generic Result down to the CursorResult text() actually returns

from sqlalchemy import CursorResult, Engine, create_engine, select, text  # => co-25: text() is the escape hatch INTO raw SQL
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Product(Base):  # => co-06: the ORM half's mapped class, used for the everyday CRUD path
    __tablename__ = "product"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    price_cents: Mapped[int]  # => cents, not a float, to avoid rounding drift (co-05 spirit)


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Product's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE product from Product's Mapped[] fields


def create_product(session: Session, name: str, price_cents: int) -> Product:  # => co-25: the ORM CRUD path -- everyday, object-shaped
    product = Product(name=name, price_cents=price_cents)  # => builds the mapped object in memory
    session.add(product)  # => registers it with the unit of work
    session.commit()  # => flushes the INSERT and assigns the auto-generated id
    return product  # => co-25: a normal ORM object, ready for the REST of the app to use as an object


def apply_holiday_discount(session: Session, percent: int) -> int:  # => co-25 + co-27: the RAW-SQL escape hatch, on the SAME session
    stmt = text("UPDATE product SET price_cents = price_cents * (100 - :pct) / 100")  # => a set-based, server-side calculation
    result = cast(CursorResult[Any], session.execute(stmt, {"pct": percent}))  # => co-25: session.execute(text()) runs raw SQL THROUGH the ORM's connection
    session.commit()  # => co-25: the SAME session, the SAME transaction boundary as the ORM path above
    return result.rowcount  # => co-25: how many rows the raw statement touched -- a fact the ORM's object API can't give this cheaply


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, shared by BOTH the ORM and raw-SQL paths
    reset_schema(engine)  # => fresh, empty product table

    with Session(engine) as session:  # => ONE session, used for BOTH the ORM creates AND the raw-SQL bulk update below
        create_product(session, "Widget", 1000)  # => co-25: everyday CRUD -- the ORM path, one object at a time
        create_product(session, "Gadget", 2000)  # => a second product, same object-shaped path
        rows_touched = apply_holiday_discount(session, percent=10)  # => co-25 + co-27: the escape hatch -- a set-based 10% cut, no loop
        prices = sorted(session.execute(select(Product.price_cents)).scalars().all())  # => co-25: back to the ORM's own select() to verify

    # => co-27: notice apply_holiday_discount() takes the SAME `Session` object -- no second engine, no second connection
    print(f"rows_touched={rows_touched}")  # => Output: rows_touched=2
    print(f"prices={prices}")  # => Output: prices=[900, 1800]
    assert rows_touched == 2  # => co-25: the raw UPDATE touched BOTH products in one statement, no per-object loop
    assert prices == [900, 1800]  # => co-25: 1000 -> 900 and 2000 -> 1800 -- a correct 10% cut, computed by Postgres itself
    # => co-25 + co-27: this is the hybrid pattern in practice -- the ORM handles per-object CRUD where its leverage
    # => helps, and `session.execute(text(...))` drops to raw SQL for the set-oriented operation it would otherwise
    # => be awkward at, WITHOUT opening a second connection or leaving the current transaction -- one session, two tiers
    print("ex-71 OK")  # => Output: ex-71 OK
