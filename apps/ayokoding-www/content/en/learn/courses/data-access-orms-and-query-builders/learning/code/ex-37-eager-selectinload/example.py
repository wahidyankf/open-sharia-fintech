# pyright: strict
"""Example 37: selectinload() -- Fixing N+1 With a SECOND, BATCHED Query."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, ForeignKey, create_engine, event, select, text  # => co-14: event captures the query COUNT
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload  # => co-14's strategy

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-14: the SAME N parents Example 36 fetched, now loaded eagerly instead
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy, OVERRIDDEN below


class CustomerOrder(Base):  # => co-14: fetched in ONE batched query for ALL parents, not one query PER parent
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK the batched IN-query filters by
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
    n_customers = 5  # => the same N as Example 36 -- the fix, not the workload, is what changes here
    # => watch the query COUNT below stay flat at 2 no matter how large n_customers grows -- that constancy is the fix
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        for i in range(n_customers):  # => seeds five customers, one order each -- identical setup to Example 36
            session.add(Customer(name=f"Customer{i}", orders=[CustomerOrder(total=Decimal("9.99"))]))
        session.commit()  # => flushes all ten rows in one batched transaction

    select_statements: list[str] = []  # => every SELECT the ORM emits during the loop below, captured for verification

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("SELECT"):  # => this example only cares about read traffic
            select_statements.append(statement)  # => keeps the FULL text for the IN-clause check below

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`

    with Session(engine) as session:  # => a FRESH session -- nothing cached, so the count reflects THIS query alone
        stmt = select(Customer).options(selectinload(Customer.orders))  # => co-14: ONE extra, TARGETED batch-load query
        customers = session.execute(stmt).scalars().all()  # => query #1 (parents) -- selectinload fires query #2 RIGHT HERE
        for customer in customers:  # => co-14: `.orders` is ALREADY loaded -- this loop touches NO new database traffic
            _ = [order.total for order in customer.orders]  # => reads from memory, not a lazy SELECT (contrast Example 36)

    print(f"customers fetched: {len(customers)}")  # => Output: customers fetched: 5
    print(f"total SELECTs: {len(select_statements)}")  # => Output: total SELECTs: 2
    assert len(select_statements) == 2  # => co-14 + co-15: ONE query for parents, ONE batched query for ALL children
    assert "customer_order.customer_id IN" in select_statements[1]  # => co-14: the SECOND query uses a single IN (...) list
    # => this IN-clause is the batching mechanism itself -- it names every parent PK collected from query #1, at once
    # => co-14: selectinload() issues `SELECT ... FROM customer_order WHERE customer_id IN (1, 2, 3, 4, 5)` -- ONE round
    # => trip covers every parent's children at once, instead of Example 36's five separate per-parent SELECTs
    print("ex-37 OK")  # => Output: ex-37 OK
