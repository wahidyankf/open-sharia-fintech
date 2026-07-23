# pyright: strict
"""Kata 5 (before): autoflush=False -- a query right after add() misses the pending row entirely."""

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

    # BUG: autoflush=False -- disables the unit of work's normal "flush pending changes before every
    # query" behavior (co-12), usually turned off ONLY for a narrow performance reason, rarely globally
    with Session(engine, autoflush=False) as session:
        session.add(Customer(name="Ada"))  # => PENDING -- no INSERT sent to Postgres yet
        count = session.execute(select(func.count()).select_from(Customer)).scalar_one()  # => intent: count includes Ada
        print(f"count_before_manual_flush={count}")  # => Output: count_before_manual_flush=0 -- Ada is invisible to THIS query
        session.rollback()  # => the pending INSERT is discarded -- Ada was never durably added at all
