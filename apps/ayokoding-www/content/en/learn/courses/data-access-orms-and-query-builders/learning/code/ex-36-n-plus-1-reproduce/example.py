# pyright: strict
"""Example 36: The N+1 Problem -- One Parent Query Fans Out Into N Child Queries."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, ForeignKey, create_engine, event, select, text  # => co-15: event captures EVERY query fired
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-15: the N parents this example loops over
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy="select"


class CustomerOrder(Base):  # => co-15: one child fetched PER PARENT the loop below touches
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK each lazy query filters by
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
    n_customers = 5  # => co-15: the "N" in "N+1" -- five parents, each with exactly one child order
    # => small ON PURPOSE: even N=5 is enough to show the pattern, and it scales linearly to real production sizes
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        for i in range(n_customers):  # => seeds five customers, one order each
            session.add(Customer(name=f"Customer{i}", orders=[CustomerOrder(total=Decimal("9.99"))]))
            # => cascades: adding the parent also registers its one child, same as Examples 22 and 34
        session.commit()  # => flushes all ten rows (5 customer + 5 customer_order) in one batched transaction

    select_statements: list[str] = []  # => every SELECT the ORM emits during the loop below, captured for verification

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("SELECT"):  # => this example only cares about read traffic
            select_statements.append(statement)  # => keeps the FULL text -- needed to tell parent SELECTs from child ones

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`

    with Session(engine) as session:  # => a FRESH session -- nothing cached, so the count below reflects THIS loop only
        customers = session.execute(select(Customer)).scalars().all()  # => query #1: the ONE parent query
        for customer in customers:  # => co-15: THIS loop is where the N+1 actually happens
            _ = [order.total for order in customer.orders]  # => co-13 + co-15: EACH iteration fires its OWN lazy SELECT

    print(f"customers fetched: {len(customers)}")  # => Output: customers fetched: 5
    print(f"total SELECTs: {len(select_statements)}")  # => Output: total SELECTs: 6
    assert len(customers) == n_customers  # => confirms the parent query itself returned all 5 rows correctly
    assert len(select_statements) == n_customers + 1  # => co-15: 1 parent query + 5 child queries = the "N+1" pattern
    # => co-15: the loop LOOKS innocent -- `customer.orders` reads like plain attribute access, not a database call --
    # => but each access is a full round trip to Postgres, and this scales LINEARLY with the number of parents fetched
    # => Example 37 fixes this exact loop with `selectinload()`, dropping the query count from N+1 down to a constant 2
    print("ex-36 OK")  # => Output: ex-36 OK
