# pyright: strict
"""Example 15: Declarative ORM Mapping -- More Mapped[] Types."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from datetime import datetime  # => co-06: Mapped[datetime] maps to a Postgres TIMESTAMP

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column  # => co-06: the ORM's typed mapping toolkit

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Product(Base):  # => co-06: a class deliberately spanning several distinct Python types
    __tablename__ = "product"  # => the physical table name this class maps to
    id: Mapped[int] = mapped_column(primary_key=True)  # => int -> INTEGER
    name: Mapped[str]  # => str -> TEXT NOT NULL
    in_stock: Mapped[bool]  # => bool -> BOOLEAN -- SQLAlchemy infers this from the Python type alone
    notes: Mapped[str | None]  # => str | None -> a NULLABLE TEXT column, using PEP 604's union syntax
    created_at: Mapped[datetime]  # => datetime -> TIMESTAMP -- round-trips as a real Python datetime, not a string


def roundtrip() -> Product:  # => returns the SAME row, reloaded fresh from Postgres in a SEPARATE session
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, shared by both sessions below
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Product's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE product from the Mapped[] fields above
    now = datetime(2026, 1, 1, 12, 0, 0)  # => a fixed timestamp -- keeps this example's output deterministic
    # => using datetime.now() here would make the printed Output different on every run
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        session.add(Product(name="Widget", in_stock=True, notes=None, created_at=now))  # => notes deliberately left NULL
        session.commit()  # => flushes and commits the INSERT in one call
        # => Product(...) here is ordinary Python object construction -- keyword args exactly match the Mapped[] fields
    with Session(engine) as session:  # => a FRESH session -- proves the values came from Postgres, not Python memory
        # => scalar_one() returns the single mapped OBJECT directly -- not a Row wrapping it, and not a list
        return session.execute(select(Product)).scalar_one()  # => scalar_one(): exactly one row, or it raises


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    product = roundtrip()  # => runs the full create -> insert -> commit -> reload cycle once
    print(f"{product.name!r} in_stock={product.in_stock} notes={product.notes!r} created_at={product.created_at}")
    # => Output: 'Widget' in_stock=True notes=None created_at=2026-01-01 12:00:00
    assert isinstance(product.in_stock, bool)  # => co-06: reloaded as a real Python bool, not the integer 0/1 Postgres stores it as
    assert product.notes is None  # => the NULL column round-tripped as Python None, not the string "None" or ""
    assert isinstance(product.created_at, datetime)  # => reloaded as a real datetime object, not an ISO-format string
    # => every Mapped[] hint above matched its RELOADED Python type -- co-06's promise made concrete, one field at a time
    print("ex-15 OK")  # => Output: ex-15 OK
