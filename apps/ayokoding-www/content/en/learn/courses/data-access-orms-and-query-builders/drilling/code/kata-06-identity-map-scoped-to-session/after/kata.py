# pyright: strict
"""Kata 6 (after): fetch through ONE shared session -- identity holds WITHIN its own identity map."""

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

    # THE FIX: fetch BOTH references through the SAME session -- co-10's identity map guarantees ONE
    # Python object per primary key WITHIN this one session, which is the guarantee it actually makes
    with Session(engine) as session:
        ada_a = session.execute(select(Customer)).scalars().one()  # => query #1
        ada_b = session.get(Customer, ada_a.id)  # => served from the identity map -- no second SELECT
    print(f"same_object_within_one_session={ada_a is ada_b}")  # => Output: same_object_within_one_session=True
    assert ada_a is ada_b  # => co-10: the guarantee holds -- scoped correctly to ONE session, as designed
