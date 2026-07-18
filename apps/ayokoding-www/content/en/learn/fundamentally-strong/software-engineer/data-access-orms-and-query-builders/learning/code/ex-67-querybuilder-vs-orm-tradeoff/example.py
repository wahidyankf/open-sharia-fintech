# pyright: strict
"""Example 67: Builder (No Identity Map) vs ORM (Change Tracking) -- a Feature/Cost Table, Demonstrated."""

from __future__ import annotations

import os  # => reads connection settings from the environment

import psycopg  # => co-26: the builder half executes via the plain DB-API -- no identity map layer at all
import psycopg.sql  # => wraps a RUNTIME str as a Composable -- psycopg's stubs require this over a plain non-literal str
from pypika import Query, Table  # => co-03: PyPika builds the SQL text, psycopg runs it
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

PG_DSN: str = os.environ.get("PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example")  # => a plain DB-API DSN
SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: the ORM half's registry root -- the builder half needs NO equivalent
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-06: a full mapped class -- the identity map keys off THIS class + primary key
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, used only by the ORM half below
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields
    with Session(engine) as session:  # => seeds exactly one row, shared by both halves below
        session.add(Customer(name="Ada"))  # => the single row both the builder AND the ORM will query TWICE
        session.commit()  # => flushes the INSERT

    customer_table = Table("customer")  # => co-26: a bare table name -- no class, no identity map possible
    rendered = str(Query.from_(customer_table).select(customer_table.id, customer_table.name))  # => rendered once, run twice below
    builder_sql = psycopg.sql.SQL(rendered)  # pyright: ignore[reportArgumentType]  # => wraps a runtime str -- not a literal, hence the escape hatch
    with psycopg.connect(PG_DSN) as conn, conn.cursor() as cur:  # => co-26: plain DB-API -- every fetch returns a FRESH tuple
        cur.execute(builder_sql)  # => first execution of the builder's SQL
        row_first = cur.fetchone()  # => co-26: a brand-new Python tuple, built fresh from THIS result set
        cur.execute(builder_sql)  # => second execution of the SAME SQL -- no caching, no dedup, by design
        row_second = cur.fetchone()  # => co-26: ANOTHER brand-new tuple -- nothing links it to the first one
    builder_same_object = row_first is row_second  # => co-26: expected False -- the builder path has no identity map at all

    with Session(engine) as session:  # => a fresh session -- the ORM half's identity map starts empty
        obj_first = session.execute(select(Customer)).scalars().one()  # => first load of the row, becomes a tracked object
        obj_second = session.execute(select(Customer)).scalars().one()  # => co-10: SAME primary key, SAME session -- identity map kicks in
    orm_same_object = obj_first is obj_second  # => co-10 + co-26: expected True -- the ORM deduplicates by primary key

    # => co-26: both halves queried the SAME row twice, in the SAME process -- the only variable is which layer sat between the driver and your code
    print(f"builder_same_object={builder_same_object}")  # => Output: builder_same_object=False
    print(f"orm_same_object={orm_same_object}")  # => Output: orm_same_object=True
    assert builder_same_object is False  # => co-26: the builder's plain rows carry NO shared identity -- two fetches, two tuples
    assert orm_same_object is True  # => co-26: the ORM's identity map turned two loads into ONE shared Python object
    # => co-26: this IS the feature/cost table, demonstrated rather than printed -- the builder pays NOTHING for
    # => identity map bookkeeping (no per-row tracking, no session, no mapped class) but also gets NOTHING back;
    # => the ORM pays setup cost (a DeclarativeBase, a mapped class, a Session) to buy deduplication AND automatic
    # => dirty-tracking (co-12) on that SAME object -- reach for the ORM specifically WHEN that tracking earns its keep
    print("ex-67 OK")  # => Output: ex-67 OK
