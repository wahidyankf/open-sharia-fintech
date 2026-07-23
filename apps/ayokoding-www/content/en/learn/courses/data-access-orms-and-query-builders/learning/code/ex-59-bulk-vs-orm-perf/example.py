# pyright: strict
"""Example 59: Measured -- Bulk Core insert() vs a Per-Object ORM Loop."""

from __future__ import annotations

import os  # => reads connection settings from the environment
import time  # => co-23: wall-clock timing -- the measured evidence, not an assumed claim

from sqlalchemy import Engine, create_engine, insert, select, text  # => co-23: insert() is the bulk path being measured
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-23: the SAME table, written twice -- once per object, once as one bulk statement
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from Customer's Mapped[] fields


def orm_loop_insert(engine: Engine, n: int) -> float:  # => co-23 + co-25: the ORM-idiomatic, per-object approach
    start = time.monotonic()  # => wall-clock start, right before the loop begins
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        for i in range(n):  # => co-23: ONE mapped object PER row, individually constructed and tracked
            session.add(Customer(name=f"Customer{i}"))  # => co-23: registers each object with the identity map, one at a time
        session.commit()  # => co-23: flushes the whole batch at once, but EACH row still got its own INSERT
    return time.monotonic() - start  # => co-23: total wall-clock time for the fully ORM-tracked path


def bulk_core_insert(engine: Engine, n: int) -> float:  # => co-23: the set-oriented, non-object approach
    start = time.monotonic()  # => wall-clock start, right before the single statement runs
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        rows = [{"name": f"Customer{i}"} for i in range(n)]  # => co-23: plain dicts -- no Customer objects, no identity map
        session.execute(insert(Customer), rows)  # => co-23: ONE Core insert(), executed with a LIST of parameter sets
        session.commit()  # => co-23: durably writes ALL rows in one batched round trip
    return time.monotonic() - start  # => co-23: total wall-clock time for the bulk, un-tracked path


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, reused across BOTH measured runs
    n_rows = 2000  # => co-23: large enough for the per-object overhead to show up clearly in wall-clock time
    # => actual measured seconds vary by machine and load -- the RATIO between the two, not the absolute numbers, is the point

    reset_schema(engine)  # => fresh, empty customer table for the ORM-loop measurement
    orm_seconds = orm_loop_insert(engine, n_rows)  # => co-25: measures the FAMILIAR, idiomatic ORM approach

    reset_schema(engine)  # => fresh, empty customer table for the bulk-Core measurement -- a fair, identical workload
    bulk_seconds = bulk_core_insert(engine, n_rows)  # => co-23: measures the SET-ORIENTED bulk approach

    with Session(engine) as session:  # => a fresh session, just to confirm BOTH approaches wrote the same row count
        final_count = len(session.execute(select(Customer)).scalars().all())  # => co-23: correctness check, not just speed

    print(f"orm loop: {orm_seconds:.3f}s")  # => Output: orm loop: 0.042s (varies by machine -- see line above)
    print(f"bulk core: {bulk_seconds:.3f}s")  # => Output: bulk core: 0.028s (varies by machine -- see line above)
    print(f"bulk is faster: {bulk_seconds < orm_seconds}")  # => Output: bulk is faster: True
    print(f"final row count: {final_count}")  # => Output: final row count: 2000
    assert final_count == n_rows  # => co-23: both paths wrote the SAME number of rows -- this is a speed test, not a correctness gap
    # => co-23: no strict `bulk_seconds < orm_seconds` assert here -- unlike a network-round-trip-dominated comparison,
    # => a modest 2000-row insert has BOTH paths batching into one executemany()-style flush at commit() (co-25), so
    # => the measured gap is pure Python-side object-construction/identity-map overhead, too thin a margin to assert
    # => on safely under CI/runner jitter; the printed ratio above is the evidence, matching Topic 26's own convention
    # => of reporting elapsed time without hard-asserting a comparison between two single-shot wall-clock measurements
    # => co-23 + co-25: the gap widens with row count -- the ORM loop pays a Python-object-construction and identity-map
    # => cost PER row that the bulk path skips entirely; for a handful of rows the difference is invisible, but for
    # => thousands of rows (data imports, batch jobs, ETL) the set-oriented bulk path is the right tool, not the ORM
    print("ex-59 OK")  # => Output: ex-59 OK
