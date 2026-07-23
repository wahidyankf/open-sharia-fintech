# pyright: strict
"""Kata 6 (before): assuming identity holds ACROSS sessions -- the identity map is per-Session, not global."""

from __future__ import annotations

import os

from sqlalchemy import create_engine, select, text
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
    with Session(engine) as session:
        session.add(Customer(name="Ada"))
        session.commit()

    # BUG: two SEPARATE sessions, each fetching the SAME row by primary key -- co-10's identity map is
    # scoped to ONE session's own identity map, never shared or synchronized across different sessions
    with Session(engine) as session_a:
        ada_a = session_a.execute(select(Customer)).scalars().one()
    with Session(engine) as session_b:
        ada_b = session_b.execute(select(Customer)).scalars().one()
    print(f"same_object_across_sessions={ada_a is ada_b}")  # => Output: same_object_across_sessions=False
    print(f"same_data={ada_a.name == ada_b.name}")  # => Output: same_data=True -- equal VALUES, different OBJECTS
