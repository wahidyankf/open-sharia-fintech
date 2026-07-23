# pyright: strict
"""Example 42: Asserting the Query Count -- Before and After an N+1 Fix, in One Script."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from collections.abc import Generator  # => the modern return-type annotation @contextmanager expects, not Iterator
from contextlib import contextmanager  # => co-15: a reusable "count queries in this block" helper
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift
from typing import Any  # => types SQLAlchemy's own untyped event-hook callback arguments

from sqlalchemy import Engine, ForeignKey, create_engine, event, select, text  # => co-15: event is the counting mechanism itself
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload  # => co-14's fix

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-15: the parents this example's assertion counts queries against
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy, OVERRIDDEN below


class CustomerOrder(Base):  # => the child whose access pattern this example counts, before and after the fix
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK every counted query touches
    total: Mapped[Decimal]  # => the order's total, as an exact Decimal
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the reverse, many-to-one navigation


def reset_and_seed(engine: Engine, n: int) -> None:  # => shared setup -- fresh schema, N customers, one order each
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fresh state for each measurement
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build both tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for both customer and customer_order
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        for i in range(n):  # => seeds N customers, one order each
            session.add(Customer(name=f"Customer{i}", orders=[CustomerOrder(total=Decimal("9.99"))]))
        session.commit()  # => flushes all rows before this measurement's own counter starts


@contextmanager  # => co-15: turns "count every SELECT fired inside this block" into a plain `with` statement
def query_counter(engine: Engine) -> Generator[list[int]]:  # => yields a one-element mutable box holding the running count
    box = [0]  # => a list, not a plain int -- the caller reads box[0] AFTER the block exits, still seeing live updates

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("SELECT"):  # => this counter only cares about read traffic
            box[0] += 1  # => increments the SAME box the caller holds a reference to

    listener = event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches for the block's duration
    try:  # => the caller's code runs HERE, between attach and detach
        yield box  # => hands the box to the `with` block -- readable both during and after
    finally:  # => detaches even if the caller's block raises
        event.remove(engine, "before_cursor_execute", listener)  # => co-15: cleanup -- the NEXT measurement starts at zero


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, reused across BEFORE and AFTER measurements
    n_customers = 5  # => the same N as Examples 36-40, so this assertion is directly comparable to those results
    # => a REAL regression test would parameterize this and assert `after_count == 2` regardless of N, catching drift

    reset_and_seed(engine, n_customers)  # => fresh workload for the BEFORE measurement
    with query_counter(engine) as before_count:  # => co-15: measures the UNFIXED, lazy-default access pattern
        with Session(engine) as session:  # => a FRESH session -- nothing cached
            customers = session.execute(select(Customer)).scalars().all()  # => query #1, the one parent query
            for customer in customers:  # => this loop is the N+1 itself -- ONE lazy SELECT per parent
                _ = [order.total for order in customer.orders]  # => co-13: each access fires its own round trip
    print(f"before fix: {before_count[0]} queries")  # => Output: before fix: 6 queries
    assert before_count[0] == n_customers + 1  # => co-15: asserts the UNFIXED count is exactly N+1, not an estimate

    reset_and_seed(engine, n_customers)  # => fresh workload for the AFTER measurement -- same shape, same size
    with query_counter(engine) as after_count:  # => co-15: measures the SAME access pattern, now eager-loaded
        with Session(engine) as session:  # => a FRESH session -- nothing cached
            stmt = select(Customer).options(selectinload(Customer.orders))  # => co-14: the fix from Example 37
            customers = session.execute(stmt).scalars().all()  # => query #1 (parents) + query #2 (batched children)
            for customer in customers:  # => identical loop, but `.orders` is now already loaded -- no new traffic
                _ = [order.total for order in customer.orders]  # => reads from memory, contributes zero new SELECTs
    print(f"after fix: {after_count[0]} queries")  # => Output: after fix: 2 queries
    assert after_count[0] == 2  # => co-15: the fix collapses N+1 down to a CONSTANT 2, regardless of how large N grows
    # => try raising n_customers to 50 or 500 and re-running -- before_count grows linearly, after_count stays at 2
    # => co-15: this is the pattern a CI regression test should assert directly -- a hard-coded query-count ceiling
    # => catches a reintroduced N+1 the moment someone accidentally removes an eager-load option, before it ships
    print("ex-42 OK")  # => Output: ex-42 OK
