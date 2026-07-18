# pyright: strict
"""Example 22: One-to-Many relationship() -- Customer -> Orders."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift

from sqlalchemy import Engine, ForeignKey, create_engine, text  # => co-08: relationship() ties two mapped classes
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-08: the "one" side of this one-to-many relationship
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-08: one customer, MANY orders
    # => the STRING "CustomerOrder" forward-references a class defined LATER in this file -- resolved at mapper config time


class CustomerOrder(Base):  # => co-08: the "many" side, named to avoid the reserved word "order"
    __tablename__ = "customer_order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the physical FK column relationship() reads
    total: Mapped[Decimal]  # => the order's total, as an exact Decimal
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => co-08: the reverse, many-to-one navigation
    # => back_populates names the OTHER side's attribute -- SQLAlchemy keeps both directions in sync in Python memory


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build both tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for both customer and customer_order


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer and customer_order tables
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Customer(name="Ada")  # => the parent object this example navigates children from
        # => `ada.orders` starts as an empty list -- relationship() manages it as a live Python collection
        ada.orders.append(CustomerOrder(total=Decimal("19.99")))  # => co-08: append() to the COLLECTION, not a raw INSERT
        ada.orders.append(CustomerOrder(total=Decimal("42.50")))  # => a second order, same collection
        session.add(ada)  # => cascades: adding the parent also registers both children -- one call, three pending rows
        session.commit()  # => flushes all three INSERTs (customer, then both customer_order rows) in dependency order
        # => co-12: the Session ordered these writes itself -- the parent's id must exist before any child's FK can

        totals = [order.total for order in ada.orders]  # => co-08: `.orders` navigates the object graph, no manual JOIN
    print(totals)  # => Output: [Decimal('19.99'), Decimal('42.50')]
    assert totals == [Decimal("19.99"), Decimal("42.50")]  # => both children came back, in insertion order
    assert all(order.customer_id == ada.id for order in ada.orders)  # => every child's FK points back at the SAME parent
    # => co-08: relationship() lets you write `ada.orders`, not `session.execute(select(CustomerOrder).where(...))`
    # => Example 34 (Intermediate tier) revisits this exact `.orders` access to show it fires a LAZY query by default
    print("ex-22 OK")  # => Output: ex-22 OK
