# pyright: strict
"""Example 55: cascade="all, delete-orphan" -- Deleting the Parent Deletes Its Children Too."""

from __future__ import annotations

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money is Decimal, never float -- exact cents, no rounding drift

from sqlalchemy import Engine, ForeignKey, create_engine, select, text  # => co-22: select() confirms the children are GONE
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-22: the parent this example deletes, taking its children along
    __tablename__ = "customer"  # => the physical table name -- NO database-level ON DELETE CASCADE here (contrast Example 56)
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list["CustomerOrder"]] = relationship(  # => co-22: cascade= is an ORM-level, Session-mediated policy
        back_populates="customer", cascade="all, delete-orphan"
    )  # => co-22: "all" propagates every session operation; "delete-orphan" also deletes a child removed from the list


class CustomerOrder(Base):  # => co-22: the child this example expects to vanish WHEN its parent is deleted through the ORM
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => a PLAIN FK -- no ON DELETE clause of its own
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
        # => cascade only fires for children the ORM has actually LOADED into this relationship collection already
        ada = Customer(  # => one parent, two children -- both should disappear once ada itself is deleted below
            name="Ada",  # => the parent this example's cascade acts on
            orders=[CustomerOrder(total=Decimal("19.99")), CustomerOrder(total=Decimal("42.50"))],  # => two children, seeded together
        )
        session.add(ada)  # => cascades: registers the parent AND both children as pending
        session.commit()  # => flushes all three INSERTs, so the delete below has real rows to remove

        session.delete(ada)  # => co-22: deletes the PARENT through the Session -- cascade="all" propagates to its children
        session.commit()  # => co-22: flushes BOTH the child DELETEs (from cascade) AND the parent's own DELETE
        # => three DELETE statements total, all inside ONE transaction -- the unit of work (co-12) orders them itself

    with Session(engine) as session:  # => a FRESH session, just to confirm the final state
        remaining_orders = session.execute(select(CustomerOrder)).scalars().all()  # => co-22: checks the CHILD table directly
        remaining_customers = session.execute(select(Customer)).scalars().all()  # => and the PARENT table too
        print(f"orders remaining: {len(remaining_orders)}")  # => Output: orders remaining: 0
        print(f"customers remaining: {len(remaining_customers)}")  # => Output: customers remaining: 0
        assert remaining_orders == [] and remaining_customers == []  # => co-22: BOTH children AND the parent are gone
    # => "delete-orphan" additionally deletes a child REMOVED from ada.orders without deleting ada itself -- "all" alone would not
    # => co-22: cascade="all, delete-orphan" makes `session.delete(ada)` propagate to every loaded child automatically --
    # => this happens entirely IN the ORM's own unit of work, issuing explicit DELETE statements for each child row,
    # => not because Postgres itself has any ON DELETE CASCADE constraint (Example 56 contrasts that alternative)
    print("ex-55 OK")  # => Output: ex-55 OK
