# pyright: strict
"""Example 34: Lazy Loading -- Accessing a Relationship Fires an EXTRA SELECT."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, ForeignKey, create_engine, event, text  # => co-13: event captures the LAZY query firing
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-13: the parent whose relationship this example accesses LAZILY
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy="select"
    # => "select" IS the default -- no lazy=... kwarg above means SQLAlchemy picks this strategy for you


class CustomerOrder(Base):  # => co-13: the child, only fetched on FIRST access of `.orders`
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK the lazy query filters by
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
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Customer(name="Ada", orders=[CustomerOrder(total=Decimal("19.99"))])  # => one parent, one child, seeded
        session.add(ada)  # => cascades: registers both the parent and the child as pending
        session.commit()  # => flushes both INSERTs
        ada_id = ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below

    statements: list[str] = []  # => every SELECT the ORM emits from here on, captured for verification below

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("SELECT"):  # => this example only cares about read traffic
            statements.append(" ".join(statement.split()[:2]).upper())  # => records "SELECT ..." -- just enough to count

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`

    with Session(engine) as session:  # => a FRESH session -- nothing cached, so the parent fetch below is a real round trip
        fetched = session.get(Customer, ada_id)  # => query #1: fetches ONLY the customer row, no orders yet
        assert fetched is not None  # => narrows Optional[Customer] for pyright --strict below
        print(f"selects after get(): {len(statements)}")  # => Output: selects after get(): 1
        # => co-13: `.orders` has NOT been touched yet -- the parent alone cost exactly one SELECT

        totals = [order.total for order in fetched.orders]  # => co-13: FIRST access of `.orders` -- fires the lazy query NOW
        print(f"selects after .orders access: {len(statements)}")  # => Output: selects after .orders access: 2
        assert len(statements) == 2  # => co-13: accessing the relationship added EXACTLY one more SELECT, on demand
        print(totals)  # => Output: [Decimal('19.99')]
        assert totals == [Decimal("19.99")]  # => the lazily-fetched child data is correct, just fetched LATE
        # => co-13: "lazy" means DEFERRED, not "free" -- the query still happens, just at first-touch instead of up front
        # => Example 37 shows the alternative: eager loading pulls this same data during the ORIGINAL query instead
    print("ex-34 OK")  # => Output: ex-34 OK
