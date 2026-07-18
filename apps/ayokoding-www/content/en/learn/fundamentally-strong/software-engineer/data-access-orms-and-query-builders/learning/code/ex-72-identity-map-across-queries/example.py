# pyright: strict
"""Example 72: The Identity Map Dedups Across TWO DIFFERENT Queries -- Not Just a Repeated One."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, ForeignKey, create_engine, select, text  # => co-10: select() is query SHAPE ONE below
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship  # => relationship() enables query SHAPE TWO

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-10: the class the identity map keys off, by primary key, within a session
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list[Order]] = relationship(back_populates="customer")  # => reached via the SECOND, different query shape


class Order(Base):  # => co-08: the "many" side -- used only to give the second query a DIFFERENT shape
    __tablename__ = "order_table"  # => named to avoid colliding with the SQL reserved word ORDER
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => the FK column backing the relationship
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the reverse navigation, exercised below


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer/Order into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE from both models' Mapped[] fields


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty schema
    with Session(engine) as session:  # => seeds ONE customer with ONE order -- both queries below reach the SAME customer row
        session.add(Customer(name="Ada", orders=[Order()]))  # => builds the whole graph in one call
        session.commit()  # => flushes both the customer and order INSERTs

    with Session(engine) as session:  # => a FRESH session -- the identity map starts empty for this run
        direct = session.execute(select(Customer).where(Customer.id == 1)).scalars().one()  # => co-10: query SHAPE ONE -- a direct PK lookup
        order = session.execute(select(Order)).scalars().one()  # => loads the Order row itself, a COMPLETELY different query
        via_relationship = order.customer  # => co-10: query SHAPE TWO -- reached by NAVIGATING a relationship, not a fresh select()
        same_object = direct is via_relationship  # => co-10: the CRITICAL check -- did the identity map dedup ACROSS these two shapes?

    print(f"same_object={same_object}")  # => Output: same_object=True
    print(f"name_via_relationship={via_relationship.name}")  # => Output: name_via_relationship=Ada
    assert same_object is True  # => co-10: a DIRECT select AND a relationship-navigation lazy load returned the IDENTICAL Python object
    # => co-10: the identity map does not care HOW a row was reached -- a top-level select(), a lazy-loaded relationship
    # => (co-13), or a JOIN would all resolve to the SAME tracked object for the SAME primary key, within ONE session;
    # => this is what makes co-12's dirty-tracking safe -- there's never more than one in-memory copy to go stale
    print("ex-72 OK")  # => Output: ex-72 OK
