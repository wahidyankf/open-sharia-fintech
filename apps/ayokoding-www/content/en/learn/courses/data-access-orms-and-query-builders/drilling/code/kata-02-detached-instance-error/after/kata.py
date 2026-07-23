# pyright: strict
"""Kata 2 (after): eager-load INSIDE the session, before it closes -- no lazy load needed afterward."""

from __future__ import annotations

import os

from sqlalchemy import ForeignKey, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload

SQLA_URL: str = os.environ.get("SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example")


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")


class CustomerOrder(Base):
    __tablename__ = "customer_order"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped[Customer] = relationship(back_populates="orders")


if __name__ == "__main__":
    engine = create_engine(SQLA_URL)
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Customer(name="Ada", orders=[]))
        session.commit()

    with Session(engine) as session:  # => THE FIX: eager-load `.orders` BEFORE the session closes
        stmt = select(Customer).options(selectinload(Customer.orders))  # => co-14: loaded up front, not on first touch
        ada = session.execute(stmt).scalars().one()
        order_count = len(ada.orders)  # => still reads it INSIDE the session, but ALREADY in memory -- no new SELECT
    # the `with` block closed here too -- `ada` is detached -- but `.orders` was already populated above
    print(f"order_count={order_count}")  # => Output: order_count=0 -- reading the SAME (empty) relationship, no error
    _ = ada.orders  # => safe: already loaded, reading a detached-but-populated collection raises nothing
    print("no error raised")  # => Output: no error raised
