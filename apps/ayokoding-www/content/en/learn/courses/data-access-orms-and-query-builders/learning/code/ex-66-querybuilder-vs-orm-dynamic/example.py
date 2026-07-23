# pyright: strict
"""Example 66: A Dynamic-Filter Query -- Builder Composes Without the Object Graph."""

from __future__ import annotations

from pypika import Field, Query, Table  # => co-03: PyPika needs only a bare Table name, no mapped class required
from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

SQLA_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"  # => used only to COMPILE the ORM statement below


class Base(DeclarativeBase):  # => co-06: the ORM half NEEDS this registry root before any query can be built
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-06: a full mapped class -- the object graph this example contrasts against PyPika
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    country: Mapped[str]  # => one of the two dynamic filter columns
    age: Mapped[int]  # => the other dynamic filter column


def build_dynamic_pypika(filters: dict[str, str | int]) -> str:  # => co-26: filters composed with NO mapped class in sight
    customer = Table("customer")  # => co-26: just a NAME -- no DeclarativeBase, no registry, no import-time schema
    query = Query.from_(customer).select(customer.id, customer.name)  # => the base SELECT, before any dynamic predicate
    for column, value in filters.items():  # => co-26: an ARBITRARY number of predicates, decided entirely at runtime
        query = query.where(Field(column) == value)  # => each iteration ANDs one more predicate onto the SAME tree
    return str(query)  # => renders the whole dynamically-built tree to SQL text on demand


def build_dynamic_orm(engine: Engine, filters: dict[str, str | int]) -> str:  # => co-26: the SAME filters, via the ORM's mapped class
    stmt = select(Customer.id, Customer.name)  # => co-06: starts from the MAPPED CLASS, not a bare table name
    for column, value in filters.items():  # => mirrors the builder loop exactly, for a fair comparison
        stmt = stmt.where(getattr(Customer, column) == value)  # => co-26: `getattr()` is needed because ORM columns are CLASS attributes
    compiled = str(stmt.compile(engine, compile_kwargs={"literal_binds": True}))  # => co-26: compiling REQUIRES the mapped class + an engine
    return " ".join(compiled.split())  # => collapses SQLAlchemy's pretty-printed newlines to one line, for a clean comparison


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => needed ONLY so the ORM half has a dialect to compile against -- never connects
    filters: dict[str, str | int] = {"country": "US", "age": 18}  # => the SAME runtime-decided filter set for both builders

    pypika_sql = build_dynamic_pypika(filters)  # => co-26: zero setup beyond a bare Table() -- no class, no registry
    orm_sql = build_dynamic_orm(engine, filters)  # => co-26: requires the FULL Customer mapped class to already exist

    print(f"pypika: {pypika_sql}")  # => Output: pypika: SELECT "id","name" FROM "customer" WHERE "country"='US' AND "age"=18
    print(f"orm: {orm_sql}")  # => Output: orm: SELECT customer.id, customer.name FROM customer WHERE customer.country = 'US' AND customer.age = 18
    # => co-26: same clean single-line rendering as the PyPika half, once SQLAlchemy's pretty-printed newlines collapse
    assert "country" in pypika_sql and "country" in orm_sql  # => co-26: both correctly compose the SAME dynamic filter set
    assert "age" in pypika_sql and "age" in orm_sql  # => co-26: both correctly compose the SECOND dynamic filter too
    # => co-26: PyPika needed ONE line (a bare Table name) before it could build ANY query -- SQLAlchemy's ORM half
    # => needed a full DeclarativeBase + Mapped[] class definition FIRST; that upfront cost buys the ORM its identity
    # => map and change tracking, but a query builder skips it entirely when all you want is composable, safe SQL
    print("ex-66 OK")  # => Output: ex-66 OK
