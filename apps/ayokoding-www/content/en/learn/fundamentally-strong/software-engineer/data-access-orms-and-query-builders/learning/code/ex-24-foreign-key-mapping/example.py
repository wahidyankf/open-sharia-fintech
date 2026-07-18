# pyright: strict
"""Example 24: ForeignKey Mapping -- the Database Enforces the Link, Not Just Python."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, ForeignKey, create_engine, text  # => co-08: ForeignKey names the referenced column
from sqlalchemy.exc import IntegrityError  # => raised when Postgres rejects a constraint violation
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-08: the referenced ("parent") table
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => the column ForeignKey("customer.id") points at
    name: Mapped[str]  # => a required TEXT column


class CustomerOrder(Base):  # => co-08: the referencing ("child") table
    __tablename__ = "customer_order"  # => named to avoid the reserved SQL word "order"
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => co-08: "table.column" string, resolved at
    # => CREATE TABLE time into a real Postgres FOREIGN KEY constraint -- this is NOT just Python bookkeeping
    # => a plain `int` column with no ForeignKey() would compile and run fine, but silently allow orphaned references
    total: Mapped[int] = mapped_column()  # => the order's total in cents, kept as a plain int for this example


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build both tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE, including the FOREIGN KEY constraint on customer_order


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer and customer_order tables, WITH the FK constraint in place

    with engine.begin() as conn:  # => inspects Postgres' own catalog -- proves the constraint is REAL, not just Python
        row = conn.execute(  # => queries information_schema for the constraint SQLAlchemy generated
            # => a raw SQL string against Postgres' system catalog -- there is no ORM class for this metadata
            text("SELECT constraint_type FROM information_schema.table_constraints WHERE table_name = 'customer_order' AND constraint_type = 'FOREIGN KEY'")
        ).fetchone()  # => None if no such constraint exists, else a one-column row
    print(f"fk constraint present: {row is not None}")  # => Output: fk constraint present: True

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        bad_order = CustomerOrder(customer_id=999, total=100)  # => 999 does NOT exist in customer -- an orphaned reference
        session.add(bad_order)  # => registers the pending insert -- no SQL sent yet
        try:  # => co-08: attempting to commit a dangling FK must fail -- Postgres enforces it, not our Python code
            session.commit()  # => flushes the INSERT -- Postgres rejects it at the database level
            raise AssertionError("expected IntegrityError")  # => this line must never run -- the commit above should raise
        except IntegrityError:  # => the expected outcome: Postgres refused the orphaned FK reference
            session.rollback()  # => co-17: undoes the failed transaction so the session is usable again
            print("insert rejected: FK constraint violated")  # => Output: insert rejected: FK constraint violated

    with Session(engine) as session:  # => a FRESH session -- confirms the customer_order table is STILL empty
        count = session.execute(text("SELECT COUNT(*) FROM customer_order")).scalar_one()  # => a raw count, no ORM class needed
        # => scalar_one(): expects exactly one row, one column -- COUNT(*) always satisfies both
    print(f"count={count}")  # => Output: count=0
    assert count == 0  # => co-08: the rejected insert left NO trace -- the FK constraint protected data integrity
    # => contrast this with a plain integer column that merely LOOKS like a foreign key in application code: without a
    # => real FOREIGN KEY constraint, Postgres would have silently accepted customer_id=999
    print("ex-24 OK")  # => Output: ex-24 OK
