# pyright: strict
"""Kata 2 (before): reading a relationship AFTER the session closed raises DetachedInstanceError."""

from __future__ import annotations

import os

from sqlalchemy import ForeignKey, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.orm.exc import DetachedInstanceError

SQLA_URL: str = os.environ.get("SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example")


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy


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

    with Session(engine) as session:  # => intent: fetch Ada, then read her orders once the query itself is done
        ada = session.execute(select(Customer)).scalars().one()
    # BUG: the `with` block above already closed -- `ada` is now DETACHED. `.orders` was never touched
    # INSIDE the session, so nothing loaded it yet -- the attempt below fires a lazy load with NO session
    try:
        _ = ada.orders  # => BUG: no open session left to run the lazy SELECT against
        print("no error raised")  # => never reached if the bug is real
    except DetachedInstanceError as exc:
        print(f"raised={type(exc).__name__}")  # => Output: raised=DetachedInstanceError
