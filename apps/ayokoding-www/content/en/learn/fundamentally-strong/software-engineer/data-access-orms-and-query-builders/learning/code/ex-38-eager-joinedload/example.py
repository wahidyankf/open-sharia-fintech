# pyright: strict
"""Example 38: joinedload() -- Fixing N+1 With ONE Single JOIN Query."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, ForeignKey, create_engine, event, select, text  # => co-14: event captures the query COUNT
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, joinedload, mapped_column, relationship  # => co-14's strategy

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-14: the SAME N parents Examples 36-37 fetched, now via a single JOIN
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy, OVERRIDDEN below


class CustomerOrder(Base):  # => co-14: fetched IN THE SAME ROW SET as its parent -- no second query at all
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK the JOIN's ON clause matches on
    total: Mapped[Decimal]  # => the order's total, as an exact Decimal
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the reverse, many-to-one navigation


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build both tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for both customer and customer_order


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer and customer_order tables
    n_customers = 5  # => the same N as Examples 36-37 -- only the loading STRATEGY changes here
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        for i in range(n_customers):  # => seeds five customers, one order each -- identical setup to Examples 36-37
            session.add(Customer(name=f"Customer{i}", orders=[CustomerOrder(total=Decimal("9.99"))]))
        session.commit()  # => flushes all ten rows in one batched transaction

    select_statements: list[str] = []  # => every SELECT the ORM emits during the query below, captured for verification

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("SELECT"):  # => this example only cares about read traffic
            select_statements.append(statement)  # => keeps the FULL text for the JOIN check below

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`

    with Session(engine) as session:  # => a FRESH session -- nothing cached, so the count reflects THIS query alone
        stmt = select(Customer).options(joinedload(Customer.orders))  # => co-14: an OUTER JOIN pulls both tables at once
        customers = session.execute(stmt).unique().scalars().all()  # => .unique() dedupes parents repeated by the JOIN
        # => co-14: without .unique(), a customer with 2+ orders would appear TWICE -- one row per JOINed match
        for customer in customers:  # => co-14: `.orders` is ALREADY loaded -- this loop touches NO new database traffic
            _ = [order.total for order in customer.orders]  # => reads from memory, populated by the single JOIN above

    print(f"customers fetched: {len(customers)}")  # => Output: customers fetched: 5
    print(f"total SELECTs: {len(select_statements)}")  # => Output: total SELECTs: 1
    assert len(select_statements) == 1  # => co-14 + co-15: ONE query total -- parents AND children in the SAME result set
    assert "LEFT OUTER JOIN customer_order" in select_statements[0]  # => co-14: the ONE query IS a JOIN, not two SELECTs
    # => co-14: joinedload() trades query COUNT for row-set SIZE -- one round trip, but a wider, sometimes-duplicated
    # => result set that needs .unique() to dedupe; selectinload() (Example 37) trades the other way: two queries, but
    # => each one stays narrow -- which strategy wins depends on how many children each parent typically has (co-14)
    print("ex-38 OK")  # => Output: ex-38 OK
