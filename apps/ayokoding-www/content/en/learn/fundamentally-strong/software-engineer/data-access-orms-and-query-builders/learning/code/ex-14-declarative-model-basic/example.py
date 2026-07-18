# pyright: strict
"""Example 14: Declarative ORM Mapping -- DeclarativeBase + Mapped[]."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import create_engine, inspect, text  # => inspect(): reads back what Postgres actually stored
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # => co-06: the ORM's typed mapping toolkit

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in a program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root that Customer below attaches to
    # => Base.metadata (used below) is the SAME concept as Core's MetaData object from Example 12


class Customer(Base):  # => co-06: a Python CLASS that is ALSO a mapped database table
    __tablename__ = "customer"  # => the physical table name this class maps to
    id: Mapped[int] = mapped_column(primary_key=True)  # => Mapped[int] -- the type hint IS the column's Python type
    name: Mapped[str]  # => Mapped[str] alone (no mapped_column()) still infers a NOT NULL TEXT column


def create_and_inspect() -> list[str]:  # => returns the column names Postgres actually stored, for verification
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine -- same engine type Core used in Examples 12-13
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => co-06: the ORM still issues plain CREATE TABLE DDL underneath
    inspector = inspect(engine)  # => Inspector reads the database's OWN catalog, independent of the Customer class
    return [col["name"] for col in inspector.get_columns("customer")]  # => what Postgres actually has, not what we assumed


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    columns = create_and_inspect()  # => creates Customer's table, then reads its columns back from Postgres itself
    print(columns)  # => Output: ['id', 'name']
    assert columns == ["id", "name"]  # => confirms the physical schema matches Customer's Mapped[] fields exactly
    # => co-06: Customer is BOTH a Python class AND a table description -- Core's Table (Example 12) was only the latter
    # => `Customer(id=1, name="Ada")` builds a normal Python object -- Example 16 shows persisting it
    print("ex-14 OK")  # => Output: ex-14 OK
