# pyright: strict
"""Kata 5 (after): the default autoflush=True flushes the pending INSERT before the SELECT runs."""

from __future__ import annotations

import os

from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get("SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example")


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


if __name__ == "__main__":
    engine = create_engine(SQLA_URL)
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(engine)

    # THE FIX: plain Session(engine) -- autoflush defaults to True, so the unit of work (co-12) flushes
    # every pending change BEFORE any query runs in the same session, keeping reads self-consistent
    with Session(engine) as session:
        session.add(Customer(name="Ada"))  # => still PENDING at this exact line -- same starting point as "before"
        count = session.execute(select(func.count()).select_from(Customer)).scalar_one()  # => autoflush fires FIRST
        print(f"count_with_default_autoflush={count}")  # => Output: count_with_default_autoflush=1 -- Ada is visible
        session.commit()
