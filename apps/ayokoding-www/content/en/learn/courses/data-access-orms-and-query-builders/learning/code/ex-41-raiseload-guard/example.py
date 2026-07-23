# pyright: strict
"""Example 41: raiseload() -- Turning an Accidental Lazy Load Into a Loud Error."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift

from sqlalchemy import Engine, ForeignKey, create_engine, select, text  # => co-16: select() is the query raiseload guards
from sqlalchemy.exc import InvalidRequestError  # => co-16: the exact exception a guarded lazy access raises
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, raiseload, relationship  # => co-16's guard

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-16: the parent this example queries WITH the raiseload guard applied
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => co-13: default lazy, GUARDED below


class CustomerOrder(Base):  # => co-16: the relationship this example forbids touching by accident
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK a lazy query would have filtered by
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
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Customer(name="Ada", orders=[CustomerOrder(total=Decimal("19.99"))])  # => one parent, one child, seeded
        session.add(ada)  # => cascades: registers both the parent and the child as pending
        session.commit()  # => flushes both INSERTs
        ada_id = ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below

    with Session(engine) as session:  # => a FRESH session -- the guard below applies to THIS query only
        stmt = select(Customer).options(raiseload(Customer.orders))  # => co-16: forbids `.orders` from ever lazy-loading
        fetched = session.execute(stmt).scalar_one()  # => fetches ONLY the customer row -- exactly like the default
        print(f"name: {fetched.name}")  # => Output: name: Ada
        # => co-16: fields already covered by the SELECT (id, name) are still perfectly readable -- only the RELATIONSHIP is guarded

        try:  # => the access below is EXACTLY what Example 36's N+1 loop did by accident, forbidden here on purpose
            _ = fetched.orders  # => co-16: touching a raiseload()-guarded relationship never silently queries
            raise AssertionError("expected InvalidRequestError")  # => fails loudly if SQLAlchemy's behavior ever changes
        except InvalidRequestError as exc:  # => co-16: a LOUD, immediate error instead of a silent extra round trip
            print(f"raised: {type(exc).__name__}")  # => Output: raised: InvalidRequestError
            # => co-16: raiseload() converts "forgot to eager-load" from a silent performance bug into a crash you catch
            # => in code review or a test run -- the SAME safety idea AsyncAttrs (co-24) applies for async sessions, where
            # => an accidental lazy load is not just slow but structurally FORBIDDEN by the driver itself (see Example 62)
    print("ex-41 OK")  # => Output: ex-41 OK
