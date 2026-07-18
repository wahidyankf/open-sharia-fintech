# pyright: strict
"""Kata 1 (after): selectinload() up front -- the property's own logic never changes."""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager
from decimal import Decimal
from typing import Any

from sqlalchemy import Engine, ForeignKey, create_engine, event, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload

SQLA_URL: str = os.environ.get("SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example")


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")

    @property
    def order_total(self) -> Decimal:  # => UNCHANGED -- the property itself was never the bug
        return sum((o.total for o in self.orders), Decimal("0"))


class CustomerOrder(Base):
    __tablename__ = "customer_order"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    total: Mapped[Decimal]
    customer: Mapped[Customer] = relationship(back_populates="orders")


@contextmanager
def query_counter(engine: Engine) -> Generator[list[int]]:
    box = [0]

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:
        if statement.strip().upper().startswith("SELECT"):
            box[0] += 1

    listener = event.listens_for(engine, "before_cursor_execute")(on_execute)
    try:
        yield box
    finally:
        event.remove(engine, "before_cursor_execute", listener)


if __name__ == "__main__":
    engine = create_engine(SQLA_URL)
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for i in range(5):
            session.add(Customer(name=f"Customer{i}", orders=[CustomerOrder(total=Decimal("9.99"))]))
        session.commit()

    with query_counter(engine) as counter:
        with Session(engine) as session:
            stmt = select(Customer).options(selectinload(Customer.orders))  # => THE FIX: eager-load BEFORE the loop
            customers = session.execute(stmt).scalars().all()  # => query #1 (parents) + query #2 (batched children)
            grand_total = sum((c.order_total for c in customers), Decimal("0"))  # => the property call site NEVER changed
    print(f"grand_total={grand_total} queries={counter[0]}")  # => Output: grand_total=49.95 queries=2
