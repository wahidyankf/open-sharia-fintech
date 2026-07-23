# pyright: strict
"""Example 40: Eager-Loading Strategy Contrast -- selectinload vs joinedload vs subqueryload."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, ForeignKey, create_engine, event, select, text  # => co-14: event captures each STRATEGY's shape
from sqlalchemy.orm import (  # => co-14: all three loading strategies compared side by side
    DeclarativeBase,  # => the shared mapper registry base for Customer/CustomerOrder below
    Mapped,  # => typed column annotation (DD-39) -- pyright --strict enforces every field
    Session,  # => the unit-of-work handle each strategy's query runs through (co-12)
    joinedload,  # => strategy #2: a single-query LEFT OUTER JOIN
    mapped_column,  # => the runtime column constructor Mapped[] pairs with
    relationship,  # => declares the one-to-many Customer.orders collection
    selectinload,  # => strategy #1: a batched, second IN-clause query
    subqueryload,  # => strategy #3: a legacy, embedded-subquery second query
)

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-14: the SAME schema Examples 36-39 used -- only the OPTIONS below change per run
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy, OVERRIDDEN per run


class CustomerOrder(Base):  # => the child whose loading strategy this example varies across three runs
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK every strategy below joins/filters on
    total: Mapped[Decimal]  # => the order's total, as an exact Decimal
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the reverse, many-to-one navigation


def reset_and_seed(engine: Engine, n_customers: int) -> None:  # => shared setup -- fresh schema, N customers, one order each
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fresh state for each strategy's run
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build both tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for both customer and customer_order
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        for i in range(n_customers):  # => seeds N customers, one order each -- IDENTICAL workload for every strategy
            session.add(Customer(name=f"Customer{i}", orders=[CustomerOrder(total=Decimal("9.99"))]))
        session.commit()  # => flushes all rows before this strategy's own query count starts being measured


def count_selects(engine: Engine, option: Any) -> int:  # => co-14: `option` is a loader-option object -- SQLAlchemy's stubs
    # => leave its precise type broad, so this ONE helper works for selectinload/joinedload/subqueryload interchangeably
    statements: list[str] = []  # => every SELECT this ONE strategy's query fires, reset per call

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("SELECT"):  # => this helper only cares about read traffic
            statements.append(statement)  # => records every SELECT text for this strategy's single query round

    listener = event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches for the duration of this call
    with Session(engine) as session:  # => a FRESH session -- nothing cached, so the count reflects THIS strategy alone
        stmt = select(Customer).options(option)  # => co-14: the ONLY thing that differs between the three calls below
        customers = session.execute(stmt).unique().scalars().all()  # => .unique() is a harmless no-op for the non-JOIN strategies
        for customer in customers:  # => touches every child so a LAZY fallback would also show up in the count
            _ = [order.total for order in customer.orders]  # => reads from memory if eager-loaded, or fires a lazy SELECT if not
    event.remove(engine, "before_cursor_execute", listener)  # => detaches so the NEXT strategy's call starts from zero
    return len(statements)  # => the total SELECT count this ONE strategy needed for the whole workload


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, reused across all three strategy runs
    n_customers = 5  # => the same N used in Examples 36-39, so the counts below are directly comparable
    reset_and_seed(engine, n_customers)  # => fresh, identical workload before the FIRST strategy's measurement
    selectin_count = count_selects(engine, selectinload(Customer.orders))  # => co-14: batched IN-clause strategy

    reset_and_seed(engine, n_customers)  # => re-seed -- each strategy measures against its OWN clean baseline
    joined_count = count_selects(engine, joinedload(Customer.orders))  # => co-14: single-query JOIN strategy

    reset_and_seed(engine, n_customers)  # => re-seed once more for the third and final strategy
    subquery_count = count_selects(engine, subqueryload(Customer.orders))  # => co-14: legacy embedded-subquery strategy

    print(f"selectinload: {selectin_count} queries")  # => Output: selectinload: 2 queries
    print(f"joinedload: {joined_count} queries")  # => Output: joinedload: 1 queries
    print(f"subqueryload: {subquery_count} queries")  # => Output: subqueryload: 2 queries
    assert (selectin_count, joined_count, subquery_count) == (2, 1, 2)  # => co-14: joinedload wins on COUNT, always 1
    # => co-14: joinedload's single query can still be the SLOWER choice once a parent has many children -- the JOIN's
    # => row set repeats every parent column once per child row, while selectinload/subqueryload keep two narrow,
    # => non-duplicated result sets; prefer selectinload() as the default modern choice, joinedload() for TRUE 1:1s,
    # => and treat subqueryload() as legacy -- present here only to recognize it when reading an older codebase
    print("ex-40 OK")  # => Output: ex-40 OK
