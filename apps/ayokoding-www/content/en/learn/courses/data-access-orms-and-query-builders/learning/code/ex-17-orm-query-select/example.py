# pyright: strict
"""Example 17: ORM Query -- session.execute(select(Model))."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, create_engine, select, text  # => co-06: select() drives the ORM, exactly like Core
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-06: the mapped class this example queries
    __tablename__ = "customer"  # => the physical table name this class maps to
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer table
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        session.add_all([Customer(name="Ada"), Customer(name="Grace")])  # => two pending objects, one call
        session.commit()  # => flushes both INSERTs and commits in one call
        # => this seeding session is fully closed before the query session below even opens

    with Session(engine) as session:  # => a FRESH session -- proves the query below re-reads from Postgres
        stmt = select(Customer).order_by(Customer.id)  # => co-06: select() targets the MAPPED CLASS, not a Core Table
        # => `stmt` composes exactly like Core's select() (Example 13) -- the ORM layers ON TOP of Core, not around it
        customers = session.execute(stmt).scalars().all()  # => .scalars(): unwraps Row -> Customer objects directly
    names = [c.name for c in customers]  # => each `c` is a live Customer OBJECT -- attribute access, not row indexing
    print(names)  # => Output: ['Ada', 'Grace']
    assert names == ["Ada", "Grace"]  # => confirms both rows returned, in id order, as typed objects
    assert all(isinstance(c, Customer) for c in customers)  # => co-06: session.execute(select(Model)) yields Model instances
    # => `customers[0].name` works right away -- no dictionary lookups, no positional tuple indexing
    # => contrast with Tier 1/2 (Examples 2, 10): those returned plain tuples -- this returns the mapped CLASS itself
    print("ex-17 OK")  # => Output: ex-17 OK
