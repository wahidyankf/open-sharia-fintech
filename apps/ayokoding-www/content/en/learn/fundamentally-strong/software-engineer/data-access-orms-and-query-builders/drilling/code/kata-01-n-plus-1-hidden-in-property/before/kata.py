# pyright: strict
"""Kata 1 (before): a "clean" loop still hides an N+1 -- the lazy load is inside a property."""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager
from decimal import Decimal
from typing import Any

from sqlalchemy import Engine, ForeignKey, create_engine, event, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get("SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example")


class Base(DeclarativeBase):
    pass


class Customer(Base):  # => the "clean" property below hides its own lazy load from every call site
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy

    @property
    def order_total(self) -> Decimal:  # => LOOKS like a plain in-memory computation from any call site
        return sum((o.total for o in self.orders), Decimal("0"))  # => BUG: `.orders` fires its OWN lazy SELECT


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
        for i in range(5):  # => 5 customers, one order each
            session.add(Customer(name=f"Customer{i}", orders=[CustomerOrder(total=Decimal("9.99"))]))
        session.commit()

    with query_counter(engine) as counter:
        with Session(engine) as session:
            customers = session.execute(select(Customer)).scalars().all()  # => query #1: the 5 parents
            grand_total = sum((c.order_total for c in customers), Decimal("0"))  # => intent: ONE clean sum expression
            # BUG: `c.order_total` is a property, but internally it still touches `.orders` -- one lazy
            # SELECT fires PER customer inside this "clean" one-liner, exactly like Example 36's raw loop
    print(f"grand_total={grand_total} queries={counter[0]}")  # => Output: grand_total=49.95 queries=6
