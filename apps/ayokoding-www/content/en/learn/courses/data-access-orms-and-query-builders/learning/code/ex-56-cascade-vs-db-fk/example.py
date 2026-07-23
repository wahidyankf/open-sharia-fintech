# pyright: strict
"""Example 56: ORM cascade vs Database ON DELETE CASCADE -- Only ONE Handles a Raw SQL Bypass."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, ForeignKey, create_engine, text  # => co-22: text() runs the RAW SQL that bypasses the ORM
from sqlalchemy.exc import IntegrityError  # => co-22: what Postgres' OWN foreign-key constraint raises when a raw delete is blocked
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class CustomerOrmOnly(Base):  # => co-22: ORM-level cascade ONLY -- Postgres itself has NO ON DELETE CASCADE on the FK
    __tablename__ = "customer_orm_only"  # => a distinct table so this half of the contrast doesn't collide with the other
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    orders: Mapped[list["OrderOrmOnly"]] = relationship(cascade="all, delete-orphan")  # => co-22: an application-level POLICY


class OrderOrmOnly(Base):  # => the child whose survival depends entirely on going THROUGH the ORM's own Session
    __tablename__ = "order_orm_only"  # => a distinct table for the ORM-only half of the contrast
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_orm_only.id"))  # => a PLAIN FK -- no ON DELETE clause


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema, rebuilt below with BOTH halves of the contrast
    Base.metadata.create_all(engine)  # => builds the ORM-managed half from the mapped classes above
    with engine.begin() as conn:  # => a second connection -- builds the RAW-SQL half with a real ON DELETE CASCADE clause
        conn.execute(text("CREATE TABLE customer_db_fk (id SERIAL PRIMARY KEY)"))  # => co-22: the DB-level parent table
        conn.execute(  # => co-22: the FK constraint ITSELF carries the cascade -- Postgres enforces it, not any Python code
            text("CREATE TABLE order_db_fk (id SERIAL PRIMARY KEY, customer_id INTEGER REFERENCES customer_db_fk(id) ON DELETE CASCADE)")
        )


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, shared by both halves of this contrast
    reset_schema(engine)  # => builds BOTH the ORM-cascade table pair and the DB-FK-cascade table pair, fresh

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        session.add(CustomerOrmOnly(id=1, orders=[OrderOrmOnly(id=1, customer_id=1)]))  # => seeds the ORM-cascade half
        session.commit()  # => flushes both rows -- explicit ids so both halves of the contrast line up for the read-back below
    with engine.begin() as conn:  # => seeds the DB-FK-cascade half with a RAW insert -- no ORM classes map to these tables
        conn.execute(text("INSERT INTO customer_db_fk (id) VALUES (1)"))  # => the DB-FK parent row
        conn.execute(text("INSERT INTO order_db_fk (id, customer_id) VALUES (1, 1)"))  # => the DB-FK child row

    orm_only_blocked = False  # => co-22: tracks whether Postgres itself refused the ORM-cascade-only bypass attempt
    try:  # => co-22: BYPASSES the ORM entirely -- a raw DELETE, no Session involved, so cascade="all, delete-orphan" NEVER runs
        with engine.begin() as conn:  # => this whole transaction rolls back automatically the moment the DELETE raises
            conn.execute(text("DELETE FROM customer_orm_only WHERE id = 1"))  # => co-22: skips the ORM's cascade policy entirely
    except IntegrityError:  # => co-22: Postgres' DEFAULT foreign-key behavior (RESTRICT) blocks a delete with live references
        orm_only_blocked = True  # => co-22: no orphan was created -- the delete was refused outright, not silently allowed

    with engine.begin() as conn:  # => co-22: the SAME raw-SQL bypass, now against the table with a REAL ON DELETE CASCADE
        conn.execute(text("DELETE FROM customer_db_fk WHERE id = 1"))  # => co-22: Postgres' own constraint handles it transparently

    with engine.begin() as conn:  # => a fresh connection to read back BOTH halves' final state
        remaining_orm_orders = conn.execute(text("SELECT * FROM order_orm_only")).fetchall()  # => co-22: still there -- the delete failed
        remaining_orm_customers = conn.execute(text("SELECT * FROM customer_orm_only")).fetchall()  # => the parent ALSO still there
        remaining_db_orders = conn.execute(text("SELECT * FROM order_db_fk")).fetchall()  # => co-22: gone -- ON DELETE CASCADE fired

    print(f"raw delete blocked without ON DELETE CASCADE: {orm_only_blocked}")  # => Output: raw delete blocked without ON DELETE CASCADE: True
    print(f"orm-only rows surviving (parent+child): {len(remaining_orm_customers) + len(remaining_orm_orders)}")  # => Output: 2
    print(f"db-fk child rows remaining: {len(remaining_db_orders)}")  # => Output: db-fk child rows remaining: 0
    assert orm_only_blocked and len(remaining_orm_customers) == 1 and len(remaining_orm_orders) == 1  # => co-22: NOTHING was deleted
    assert len(remaining_db_orders) == 0  # => co-22: Postgres' own ON DELETE CASCADE fired regardless of HOW the parent was deleted
    # => co-22: ORM cascade is a Session-level POLICY -- it only runs when a delete goes through session.delete(); a raw
    # => SQL DELETE that bypasses the Session gets NEITHER the ORM's cascade NOR any orphaning -- Postgres' own default
    # => foreign-key behavior (RESTRICT) simply refuses the delete outright, which is safer than silently orphaning rows
    # => but still surprising if you expected `cascade="all, delete-orphan"` to protect every deletion path. A real
    # => ON DELETE CASCADE constraint is enforced by Postgres ITSELF, for every deletion path, with no exceptions --
    # => reach for it whenever data integrity must hold regardless of which code path performs the delete
    print("ex-56 OK")  # => Output: ex-56 OK
