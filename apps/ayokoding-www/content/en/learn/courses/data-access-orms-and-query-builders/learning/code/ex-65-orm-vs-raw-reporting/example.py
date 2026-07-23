# pyright: strict
"""Example 65: A Reporting Query -- ORM Object-Loading Is Awkward, Raw SQL Wins for Set Operations."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, ForeignKey, create_engine, select, text  # => co-06: the ORM half loads mapped objects
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-08: the "one" side, this report ranks customers by total order value
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list[Order]] = relationship(back_populates="customer")  # => the collection the ORM half must load and sum in Python


class Order(Base):  # => co-08: the "many" side -- amount_cents is what the report aggregates
    __tablename__ = "order_table"  # => named to avoid colliding with the SQL reserved word ORDER
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK column backing the relationship
    amount_cents: Mapped[int]  # => cents, not a float, to avoid rounding drift (co-05 spirit)
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the reverse navigation, unused by this report


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer/Order into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE from both models' Mapped[] fields


def report_orm(engine: Engine) -> tuple[str, int]:  # => co-25 + co-27: the object-shaped, in-Python-aggregation path
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        stmt = select(Customer).options(selectinload(Customer.orders))  # => co-14: loads EVERY customer AND every order into Python
        customers = session.execute(stmt).scalars().all()  # => the whole table, pulled into memory as mapped objects
        totals = [(c.name, sum(o.amount_cents for o in c.orders)) for c in customers]  # => co-25: aggregation done by HAND, in Python
        top = max(totals, key=lambda pair: pair[1])  # => co-25: another manual pass, just to find the max -- SQL would do this in one clause
    return top  # => co-25: correct, but every step (load, sum, sort) is Python work Postgres could have done itself


def report_raw(engine: Engine) -> tuple[str, int]:  # => co-25 + co-27: the SAME report as one set-oriented SQL statement
    # => co-25: GROUP BY + SUM + ORDER BY + LIMIT, ALL computed server-side, in a single round trip
    # => co-27: this ENTIRE report is one statement -- no Python loop, no manual max(), no intermediate objects
    sql = text("SELECT c.name, SUM(o.amount_cents) AS total FROM customer c JOIN order_table o ON o.customer_id = c.id GROUP BY c.id, c.name ORDER BY total DESC LIMIT 1")
    with engine.connect() as conn:  # => a plain connection -- no ORM objects, no identity map, needed for a pure aggregate
        row = conn.execute(sql).one()  # => co-25: ONE query returns the ALREADY-AGGREGATED answer, no Python-side math
    return (row.name, row.total)  # => co-25: the database did the summing, grouping, and ranking -- Python just reads the result


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, shared by both reporting paths
    reset_schema(engine)  # => fresh, empty schema before seeding

    with Session(engine) as session:  # => seeds two customers with different total order values
        ada = Customer(name="Ada", orders=[Order(amount_cents=500), Order(amount_cents=700)])  # => Ada totals 1200
        grace = Customer(name="Grace", orders=[Order(amount_cents=2000)])  # => Grace totals 2000 -- the expected winner
        session.add_all([ada, grace])  # => registers both customers and their nested orders in one call
        session.commit()  # => flushes every INSERT for both customers and all three orders

    orm_top = report_orm(engine)  # => co-25: runs the object-loading, Python-aggregation path
    raw_top = report_raw(engine)  # => co-25: runs the set-oriented, server-side-aggregation path

    print(f"orm_top={orm_top}")  # => Output: orm_top=('Grace', 2000)
    print(f"raw_top={raw_top}")  # => Output: raw_top=('Grace', 2000)
    assert orm_top == raw_top == ("Grace", 2000)  # => co-25: both paths agree on the SAME correct answer
    # => co-25 + co-27: for a report like this, raw SQL is not just shorter -- it is CORRECT BY CONSTRUCTION at any
    # => scale, because the aggregation runs where the data lives; the ORM path must first materialize EVERY row as
    # => a Python object before it can even start summing, which is wasted memory and network traffic at real scale
    print("ex-65 OK")  # => Output: ex-65 OK
