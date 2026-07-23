# pyright: strict
"""Kata 4 (after): cascade="all, delete-orphan" -- deleting the parent deletes its orders too."""

from __future__ import annotations

import os

from sqlalchemy import ForeignKey, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get("SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example")


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    # THE FIX: cascade="all, delete-orphan" -- the ORM now issues DELETE FROM customer_order BEFORE
    # DELETE FROM customer, instead of trying (and failing) to null out a NOT NULL FK column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer", cascade="all, delete-orphan")


class CustomerOrder(Base):
    __tablename__ = "customer_order"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), nullable=False)
    customer: Mapped[Customer] = relationship(back_populates="orders")


if __name__ == "__main__":
    engine = create_engine(SQLA_URL)
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Customer(name="Ada", orders=[CustomerOrder()]))
        session.commit()

    with Session(engine) as session:
        ada = session.execute(select(Customer)).scalars().one()
        session.delete(ada)
        session.commit()  # => THE FIX: succeeds -- the ORM deletes the order row first, then the customer row

    with Session(engine) as session:
        remaining_customers = session.execute(select(Customer)).scalars().all()
        remaining_orders = session.execute(select(CustomerOrder)).scalars().all()
    print(f"remaining_customers={len(remaining_customers)} remaining_orders={len(remaining_orders)}")  # => Output: remaining_customers=0 remaining_orders=0
