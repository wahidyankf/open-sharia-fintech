# pyright: strict
"""Example 73: Configuring the DEFAULT Lazy Strategy Per Relationship -- No Per-Query .options() Needed."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from collections.abc import Generator  # => the modern return-type annotation @contextmanager expects, not Iterator
from contextlib import contextmanager  # => co-15: a reusable "count queries in this block" helper, reused from Example 42
from typing import Any  # => types SQLAlchemy's own untyped event-hook callback arguments

from sqlalchemy import Engine, ForeignKey, create_engine, event, select, text  # => co-15: event is the counting mechanism
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship  # => co-14: relationship(lazy=...) is the config knob

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-13 + co-14: the relationship below carries its OWN default strategy, set once, here
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list[Order]] = relationship(back_populates="customer", lazy="selectin")  # => co-14: CONFIGURED, not per-query


class Order(Base):  # => the child every plain select(Customer) below implicitly eager-loads, with no .options() call
    __tablename__ = "order_table"  # => named to avoid colliding with the SQL reserved word ORDER
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK column backing the relationship
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the reverse navigation, still plain-lazy by default


def reset_and_seed(engine: Engine, n: int) -> None:  # => shared setup -- fresh schema, N customers, one order each
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fresh state for each measurement
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build both tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for both customer and order_table
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        for i in range(n):  # => seeds N customers, one order each
            session.add(Customer(name=f"Customer{i}", orders=[Order()]))  # => a Customer plus exactly one child Order
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
        event.remove(engine, "before_cursor_execute", listener)  # => cleanup -- the NEXT measurement starts at zero


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    n_customers = 5  # => enough parents to make a per-object N+1 visibly different from a constant-2 query count
    reset_and_seed(engine, n_customers)  # => fresh workload for this measurement

    with query_counter(engine) as count:  # => co-14: measures a PLAIN select(Customer), NO .options() at the call site
        with Session(engine) as session:  # => a FRESH session -- nothing cached
            customers = session.execute(select(Customer)).scalars().all()  # => query #1 -- the configured lazy="selectin" fires HERE too
            for customer in customers:  # => touching `.orders` costs NOTHING new -- it was already batch-loaded
                _ = [order.id for order in customer.orders]  # => co-14: reads from memory, zero additional round trips

    print(f"query_count={count[0]}")  # => Output: query_count=2
    assert count[0] == 2  # => co-14: exactly 2 queries -- the SAME shape as Example 37's explicit selectinload(), for free
    # => co-14: `lazy="selectin"` in the relationship() DEFINITION changes the DEFAULT for EVERY query against this
    # => class -- no caller needs to remember `.options(selectinload(...))`; the trade-off is that EVERY access to
    # => `.orders` now eager-loads, even in code paths that never touch the relationship, so choose it deliberately
    print("ex-73 OK")  # => Output: ex-73 OK
