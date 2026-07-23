# pyright: strict
"""Example 1: Spectrum -- Same Query, Three Ways."""

from __future__ import annotations  # => lets `"CustomerOrder"` below resolve as a forward-referenced type

import os  # => stdlib: reads connection settings from the environment (co-01)
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift
from typing import LiteralString, cast  # => acknowledges a runtime-built string is safe to execute (see tier2)

import psycopg  # => Tier 1 + Tier 2 both execute through the raw PEP 249 DB-API (co-02)
from pypika import Order as SortDir  # => PyPika's ASC/DESC enum -- renamed to avoid our own `Order` name
from pypika import Query, Table  # => Tier 2: PyPika builds the query as composable Python values (co-03)
from sqlalchemy import ForeignKey, create_engine, select  # => Tier 3: the SQLAlchemy ORM (co-06)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship  # => the ORM's typed mapping toolkit

PG_HOST: str = os.environ.get("PG_HOST", "localhost")  # => override for CI / non-default hosts
PG_PORT: str = os.environ.get("PG_PORT", "5432")  # => Postgres' conventional default port
PG_DB: str = os.environ.get("PG_DB", "orm_by_example")  # => one shared database, every example resets its own tables
PG_USER: str = os.environ.get("PG_USER", "postgres")  # => local trust-auth Postgres convention
PG_PASSWORD: str = os.environ.get("PG_PASSWORD", "postgres")  # => matches PG_USER for local dev
PG_DSN: str = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"  # => plain DB-API DSN (Tiers 1-2)
SQLA_URL: str = f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"  # => SQLAlchemy dialect+driver URL (Tier 3)


def seed_schema() -> None:
    """Reset and seed the shared `customer`/`customer_order` tables (raw SQL -- co-02)."""
    # => every example in this topic owns and resets its own tables -- self-contained, run-in-any-order
    with psycopg.connect(PG_DSN, autocommit=True) as conn:  # => autocommit: DDL needs no explicit commit
        conn.execute("DROP SCHEMA public CASCADE")  # => wipes EVERY table, including any left behind by a DIFFERENT example
        conn.execute("CREATE SCHEMA public")  # => a blank public schema -- fully isolated, run-in-any-order (self-contained)
        conn.execute("CREATE TABLE customer(id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL)")  # => the "one" side of the relationship
        conn.execute("CREATE TABLE customer_order(id SERIAL PRIMARY KEY, customer_id INT NOT NULL REFERENCES customer(id), total NUMERIC(10,2) NOT NULL)")  # => FK ties every order to one customer
        # => customer_order deliberately avoids the bare word "order" -- a reserved SQL keyword every tier would have to quote
        conn.execute("INSERT INTO customer(name, email) VALUES ('Ada', 'ada@example.com'), ('Grace', 'grace@example.com')")  # => two customers, ids 1 and 2
        conn.execute("INSERT INTO customer_order(customer_id, total) VALUES (1, 19.99), (1, 42.50), (2, 8.00)")  # => two orders for Ada, one for Grace


def tier1_raw_sql() -> list[tuple[int, str, Decimal]]:  # => co-01: tier 1 of 3 -- the raw-SQL floor
    """Tier 1: hand-written SQL over the PEP 249 DB-API (co-02) -- the floor of the spectrum."""
    with psycopg.connect(PG_DSN) as conn:  # => a fresh connection -- no builder, no ORM in between
        rows = conn.execute(  # => a plain string-literal JOIN -- nothing composes it for you
            "SELECT o.id, c.name, o.total FROM customer_order o JOIN customer c ON c.id = o.customer_id ORDER BY o.id"
            # => every table name, join condition, and column is typed out by hand as literal text
        ).fetchall()  # => fetchall() materializes every row as a list of tuples right now
    # => psycopg's default row type is a plain, untyped tuple -- Example 4 upgrades this to a typed dataclass
    return [(int(r[0]), str(r[1]), Decimal(r[2])) for r in rows]  # => cast each column so all 3 tiers compare equal


def tier2_query_builder() -> list[tuple[int, str, Decimal]]:  # => co-01: tier 2 of 3 -- the query-builder middle
    """Tier 2: the SAME join, composed as data via PyPika (co-03) -- no string concatenation."""
    order_tbl = Table("customer_order", alias="o")  # => a Table VALUE, not a string -- co-03's core idea
    cust_tbl = Table("customer", alias="c")  # => composable, so it can be reused across multiple queries
    # => co-04: PyPika is a standalone builder library -- Example 12 contrasts it with SQLAlchemy Core's own builder
    query = (
        Query.from_(order_tbl)  # => start the builder tree from customer_order
        .join(cust_tbl)  # => .join() takes another Table value, not a raw "JOIN ..." string
        .on(cust_tbl.id == order_tbl.customer_id)  # => .on() takes a PyPika expression object, not text
        .select(order_tbl.id, cust_tbl.name, order_tbl.total)  # => column list is also composed, not interpolated
        .orderby(order_tbl.id, order=SortDir.asc)  # => ORDER BY is composed the same way as every other clause
    )  # => the tree only becomes SQL text when you ask for it -- nothing has run yet
    with psycopg.connect(PG_DSN) as conn:  # => the SAME DB-API tier executes PyPika's rendered output
        sql_text = cast(LiteralString, str(query))  # => str(query) renders the tree; cast() vouches it is safe to run
        rows = conn.execute(sql_text).fetchall()  # => the DB-API executes PyPika's OUTPUT exactly like Tier 1's own SQL
    # => same DB-API, same tuple rows -- only HOW the SQL text got built differs from Tier 1
    return [(int(r[0]), str(r[1]), Decimal(r[2])) for r in rows]  # => same normalization as Tier 1, for comparison


class Base(DeclarativeBase):  # => co-06: the shared declarative base every mapped class inherits from
    pass  # => carries no columns itself -- purely a registry root for Tier 3's classes below
    # => every DeclarativeBase subclass shares ONE registry -- relationship() lookups (co-08) resolve through it


class Customer(Base):  # => Tier 3's "one" side, mapped from the SAME customer table Tiers 1-2 read
    __tablename__ = "customer"  # => must match the physical table name exactly
    id: Mapped[int] = mapped_column(primary_key=True)  # => Mapped[int] -- co-06's typed column mapping
    name: Mapped[str]  # => column type inferred from the Python type alone -- no mapped_column() needed here
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-08: one customer, many orders


class CustomerOrder(Base):  # => Tier 3's "many" side, mapped from customer_order
    __tablename__ = "customer_order"  # => again, must match the physical table name exactly
    id: Mapped[int] = mapped_column(primary_key=True)  # => same shape as Customer.id -- every mapped class needs a PK
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => co-08: the physical FK column
    total: Mapped[Decimal]  # => Mapped[Decimal] round-trips Postgres NUMERIC without precision loss
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => co-08: the reverse navigation, order -> customer


def tier3_orm() -> list[tuple[int, str, Decimal]]:  # => co-01: tier 3 of 3 -- the full ORM ceiling
    """Tier 3: the SAME join, expressed as an object graph via the SQLAlchemy ORM (co-06)."""
    engine = create_engine(SQLA_URL)  # => the engine still emits SQL underneath -- the ORM never bypasses it
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12) -- opened per request
        stmt = select(CustomerOrder).join(Customer).order_by(CustomerOrder.id)  # => join() infers the FK -- no raw ON clause written
        # => `stmt` is itself a builder tree, much like Tier 2's `query` -- the ORM layers ON TOP of Core, not around it
        results = session.execute(stmt).scalars().all()  # => .scalars() unwraps Row -> CustomerOrder objects directly
        # => `results` is a list of live CustomerOrder objects, not tuples -- this is what "object graph" means
        return [(o.id, o.customer.name, o.total) for o in results]  # => .customer navigates the object graph (co-13, lazy, session still open)


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    seed_schema()  # => one shared dataset every tier below reads -- proves they agree on the SAME rows
    r1 = tier1_raw_sql()  # => run Tier 1
    r2 = tier2_query_builder()  # => run Tier 2
    r3 = tier3_orm()  # => run Tier 3
    print(f"tier1_raw_sql:       {r1}")  # => Output: tier1_raw_sql:       [(1, 'Ada', Decimal('19.99')), (2, 'Ada', Decimal('42.50')), (3, 'Grace', Decimal('8.00'))]
    print(f"tier2_query_builder: {r2}")  # => Output: tier2_query_builder: [(1, 'Ada', Decimal('19.99')), (2, 'Ada', Decimal('42.50')), (3, 'Grace', Decimal('8.00'))]
    print(f"tier3_orm:           {r3}")  # => Output: tier3_orm:           [(1, 'Ada', Decimal('19.99')), (2, 'Ada', Decimal('42.50')), (3, 'Grace', Decimal('8.00'))]
    assert r1 == r2 == r3  # => co-01's whole point: three tiers, one set of rows -- style differs, the answer doesn't
    # => the rest of this topic picks ONE tier per concept -- keep this comparison in mind as the throughline
    print("ex-01 OK")  # => Output: ex-01 OK
