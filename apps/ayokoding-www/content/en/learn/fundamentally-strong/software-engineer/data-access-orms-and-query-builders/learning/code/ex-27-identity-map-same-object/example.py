# pyright: strict
"""Example 27: Identity Map -- Two Queries, One Python Object."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, create_engine, select, text  # => co-10: select() is how the identity map gets exercised
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-10: the mapped class whose identity this example tracks
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => the primary key the identity map keys ITSELF by
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
        ada = Customer(name="Ada")  # => the one row this example queries twice
        session.add(ada)  # => registers `ada` as pending
        session.commit()  # => flushes the INSERT, assigns ada.id
        ada_id = ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError below

        first = session.execute(select(Customer).where(Customer.id == ada_id)).scalar_one()  # => query #1, by PK
        # => co-10: SQLAlchemy DID send a SELECT to Postgres here -- the identity map does not skip round-trips
        second = session.get(Customer, ada_id)  # => query #2, a DIFFERENT API (session.get) for the SAME PK, SAME session
        third = session.execute(select(Customer).where(Customer.id == ada_id)).scalar_one()  # => query #3, back to select()

        print(f"first is second: {first is second}")  # => Output: first is second: True
        print(f"second is third: {second is third}")  # => Output: second is third: True
        assert first is second is third  # => co-10: three DIFFERENT query calls, but ONE Python object came back every time
        # => co-10: the Session's identity map maps (class, primary key) -> the ONE Python object it already built for that
        # => row -- later lookups by the SAME PK, in the SAME session, return the SAME object instead of a fresh copy
        # => this matters for mutation: changing `first.name` also changes what `second` and `third` see -- they ARE it

    with Session(engine) as session:  # => a FRESH session -- the identity map is scoped PER session, not global
        outside = session.get(Customer, ada_id)  # => a brand-new object, because this is a brand-new session's own map
    print(f"outside is first: {outside is first}")  # => Output: outside is first: False
    assert outside is not first  # => co-10: crossing a session boundary breaks object identity -- a NEW map, a NEW object
    print("ex-27 OK")  # => Output: ex-27 OK
