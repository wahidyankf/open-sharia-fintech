# pyright: strict
"""Example 35: Lazy Loading After Session Close -- DetachedInstanceError."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift

from sqlalchemy import Engine, ForeignKey, create_engine, text  # => co-13: relationship() is what needs the LIVE session
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.orm.exc import DetachedInstanceError  # => co-13/co-11: the exact exception a detached lazy access raises

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-11: the object this example detaches by closing its owning session
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column, safe to read even after detach -- it was already loaded
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: NOT loaded yet, on purpose


class CustomerOrder(Base):  # => the child, deliberately left un-accessed until AFTER the session closes
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK the lazy query would filter by
    total: Mapped[Decimal]  # => the order's total, as an exact Decimal
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the reverse, many-to-one navigation


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build both tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for both customer and customer_order


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer and customer_order tables
    session = Session(engine)  # => opened WITHOUT a `with` block -- this example controls the close() moment explicitly
    ada = Customer(name="Ada", orders=[CustomerOrder(total=Decimal("19.99"))])  # => one parent, one child, seeded
    session.add(ada)  # => cascades: registers both the parent and the child as pending
    session.commit()  # => flushes both INSERTs -- ada is now PERSISTENT, still attached to `session`

    print(f"name while attached: {ada.name}")  # => Output: name while attached: Ada
    # => co-13: `.name` is safe -- it was already loaded into `ada.__dict__` by the commit's own refresh, no query needed

    session.close()  # => co-11: STAGE 4 -- CLOSE. ada is now DETACHED -- no session backs it anymore
    print(f"name after close: {ada.name}")  # => Output: name after close: Ada
    # => co-11: still safe -- `name` was ALREADY loaded, so reading it needs no round trip to Postgres at all

    try:  # => the access below NEEDS a live session, because `.orders` was never touched before close()
        _ = ada.orders  # => co-13: first access of an UNLOADED relationship on a DETACHED object -- no session to query with
        raise AssertionError("expected DetachedInstanceError")  # => co-13: fails loudly if SQLAlchemy's behavior ever changes
    except DetachedInstanceError as exc:  # => co-13 + co-11: the ORM refuses to silently return an empty/wrong list
        print(f"raised: {type(exc).__name__}")  # => Output: raised: DetachedInstanceError
        # => co-13: this is EXACTLY the failure mode eager loading (Example 37) or `AsyncAttrs` (co-16/co-24) sidesteps --
        # => a lazy attribute is a promise to query LATER, and "later" must still be inside a session that is still open
    print("ex-35 OK")  # => Output: ex-35 OK
