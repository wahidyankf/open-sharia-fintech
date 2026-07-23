# pyright: strict
"""Example 23: Bidirectional back_populates -- Both Sides Stay Linked."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift

from sqlalchemy import Engine, ForeignKey, create_engine, text  # => co-08: back_populates keeps two sides in sync
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-08: the "one" side of this relationship
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")  # => names CustomerOrder.customer below
    # => this string MUST exactly match the attribute name relationship() reads on the OTHER class -- a typo here fails at
    # => mapper-configuration time, not silently at runtime


class CustomerOrder(Base):  # => co-08: the "many" side
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the physical FK column
    total: Mapped[Decimal]  # => the order's total, as an exact Decimal
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => names Customer.orders above -- the OTHER half
    # => co-08: two relationship() calls, each pointing at the OTHER side's attribute name -- this pairing is what
    # => "bidirectional" means: SQLAlchemy keeps `.orders` and `.customer` mutually consistent in Python memory


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build both tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for both customer and customer_order


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer and customer_order tables

    ada = Customer(name="Ada")  # => the parent side of this bidirectional pair
    order = CustomerOrder(total=Decimal("19.99"))  # => the child side -- note it has NO customer set yet
    order.customer = ada  # => co-08: setting ONE side of back_populates -- watch the OTHER side below
    print(f"ada.orders contains order: {order in ada.orders}")  # => Output: ada.orders contains order: True
    # => co-08: setting `order.customer = ada` automatically appended `order` into `ada.orders` too -- IN PYTHON MEMORY,
    # => before ANY database round-trip happened -- back_populates keeps both collections mutually consistent

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        session.add(ada)  # => cascades: adding the parent registers the linked child too
        session.commit()  # => flushes both rows, in dependency order
        order_id = order.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below
        customer_id = ada.id  # => same reason -- read now, while the session is still open

    with Session(engine) as session:  # => a FRESH session -- reloads from Postgres, proving the FK actually persisted
        reloaded = session.get(CustomerOrder, order_id)  # => session.get(): a single-PK lookup, no explicit select() needed
        assert reloaded is not None  # => the row exists -- session.get() returns None only for a missing PK
        print(f"reloaded.customer_id={reloaded.customer_id}")  # => Output: reloaded.customer_id=1
        assert reloaded.customer_id == customer_id  # => the FK column on disk matches the in-memory link from earlier
    print("ex-23 OK")  # => Output: ex-23 OK
