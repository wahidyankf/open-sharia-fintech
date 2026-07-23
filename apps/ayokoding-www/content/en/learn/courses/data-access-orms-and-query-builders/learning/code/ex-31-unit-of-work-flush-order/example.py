# pyright: strict
"""Example 31: Unit of Work -- the Session Orders INSERTs by Dependency, Not by Code Order."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from typing import Any  # => the event hook's callback signature is untyped by SQLAlchemy's own stubs

from sqlalchemy import Engine, ForeignKey, create_engine, event, text  # => co-12: event captures the ACTUAL flush order
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-12: the PARENT -- its row must exist before any child's FK can reference it
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => the PK the child FK depends on
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => the parent-to-child collection


class CustomerOrder(Base):  # => co-12: the CHILD -- its FK depends on the parent's PK already existing
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the dependency the unit of work must respect
    total: Mapped[int] = mapped_column()  # => the order's total in cents, kept as a plain int for this example
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the child-to-parent reverse link


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build both tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for both customer and customer_order


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer and customer_order tables

    statements: list[str] = []  # => every SQL statement the ORM emits, captured for verification below

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        statements.append(" ".join(statement.split()[:3]).upper())  # => records "INSERT INTO <table>" -- verb AND target

    event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches the hook to every statement on `engine`

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        order = CustomerOrder(total=1999)  # => co-12: the CHILD object is constructed and added FIRST, out of dependency order
        # => deliberately backwards -- proves the unit of work computes dependency order itself, not just source order
        ada = Customer(name="Ada")  # => the PARENT object, constructed SECOND -- code order says child, then parent
        order.customer = ada  # => links them -- back_populates keeps ada.orders in sync too
        session.add(order)  # => registers the child FIRST, matching the CODE order above
        session.add(ada)  # => registers the parent SECOND, again matching the CODE order above
        session.commit()  # => co-12: flushes both -- but NOT in the order they were added

    insert_statements = [s for s in statements if s.startswith("INSERT")]  # => filters to the two INSERTs this example expects
    print(insert_statements)  # => Output: ['INSERT INTO CUSTOMER', 'INSERT INTO CUSTOMER_ORDER']
    assert insert_statements == ["INSERT INTO CUSTOMER", "INSERT INTO CUSTOMER_ORDER"]  # => customer landed FIRST
    # => co-12: the unit of work reordered these writes ITSELF -- it inspected the FK dependency (order.customer_id ->
    # => customer.id) and inserted customer BEFORE customer_order, even though `order` was added to the session first
    # => this is the defining trait of Unit of Work: the caller declares WHAT changed, the pattern decides WHEN to write it
    print("ex-31 OK")  # => Output: ex-31 OK
