# pyright: strict
"""Example 39: subqueryload() -- a LEGACY Batched Strategy, Superseded by selectinload()."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, ForeignKey, create_engine, event, select, text  # => co-14: event captures the query COUNT
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, subqueryload  # => co-14's LEGACY strategy

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-14: the SAME N parents Examples 36-38 fetched, now via subqueryload
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy, OVERRIDDEN below


class CustomerOrder(Base):  # => co-14: fetched via a SEPARATE query that RE-RUNS the original SELECT as a subquery
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK the batched subquery filters by
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
    n_customers = 5  # => the same N as Examples 36-38 -- only the loading STRATEGY changes here
    # => keeping the workload identical across Examples 36-39 is what makes the query-count contrast in Example 40 fair
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        for i in range(n_customers):  # => seeds five customers, one order each -- identical setup to Examples 36-38
            session.add(Customer(name=f"Customer{i}", orders=[CustomerOrder(total=Decimal("9.99"))]))
        session.commit()  # => flushes all ten rows in one batched transaction

    select_statements: list[str] = []  # => every SELECT the ORM emits during the query below, captured for verification

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("SELECT"):  # => this example only cares about read traffic
            select_statements.append(statement)  # => keeps the FULL text for the subquery check below

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`

    with Session(engine) as session:  # => a FRESH session -- nothing cached, so the count reflects THIS query alone
        stmt = select(Customer).options(subqueryload(Customer.orders))  # => co-14: LEGACY -- re-embeds the ORIGINAL query
        customers = session.execute(stmt).scalars().all()  # => query #1 (parents); subqueryload fires query #2 RIGHT HERE
        for customer in customers:  # => co-14: `.orders` is ALREADY loaded -- this loop touches NO new database traffic
            _ = [order.total for order in customer.orders]  # => reads from memory, populated by the second query above

    print(f"customers fetched: {len(customers)}")  # => Output: customers fetched: 5
    print(f"total SELECTs: {len(select_statements)}")  # => Output: total SELECTs: 2
    assert len(select_statements) == 2  # => co-14: also 2 queries, like selectinload -- the difference is HOW #2 filters
    assert "FROM (SELECT customer.id AS customer_id" in select_statements[1]  # => co-14: an embedded subquery re-derives the parents
    # => co-14: SQLAlchemy's own docs now call subqueryload() "mostly legacy" -- selectinload() (Example 37) does the
    # => SAME job with a simpler, more predictable IN (...) list instead of re-running the parent query as a correlated
    # => subquery; prefer selectinload() in new code -- subqueryload() mainly still matters for reading OLDER codebases
    print("ex-39 OK")  # => Output: ex-39 OK
