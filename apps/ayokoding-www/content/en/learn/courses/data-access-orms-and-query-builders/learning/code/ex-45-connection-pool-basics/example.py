# pyright: strict
"""Example 45: pool_size and max_overflow -- Connections Reused, Not Reopened Per Query."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import create_engine, text  # => co-18: the engine owns the pool every connection borrows from
from sqlalchemy.pool import QueuePool  # => co-18: the default pool implementation this example inspects directly

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance

if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL, pool_size=2, max_overflow=1)  # => co-18: at most 2 PERSISTENT + 1 overflow connection
    pool = engine.pool  # => co-18: the actual QueuePool object -- inspectable at runtime, not just a config knob
    assert isinstance(pool, QueuePool)  # => confirms the DEFAULT pool class -- narrows the type for pyright --strict below

    print(f"checked out before use: {pool.checkedout()}")  # => Output: checked out before use: 0
    # => co-18: create_engine() does NOT open any connections up front -- the pool starts completely empty

    with engine.connect() as conn1:  # => co-18: borrows connection #1 FROM the pool -- opens a NEW physical connection
        pid1 = conn1.execute(text("SELECT pg_backend_pid()")).scalar_one()  # => Postgres' own process id for THIS connection
        print(f"checked out with 1 open: {pool.checkedout()}")  # => Output: checked out with 1 open: 1

        with engine.connect() as conn2:  # => borrows connection #2 -- ALSO a new physical connection, still within pool_size
            pid2 = conn2.execute(text("SELECT pg_backend_pid()")).scalar_one()  # => a DIFFERENT backend pid than conn1's
            print(f"checked out with 2 open: {pool.checkedout()}")  # => Output: checked out with 2 open: 2
            assert pid1 != pid2  # => co-18: two SIMULTANEOUS connections are genuinely two separate Postgres backends

    print(f"checked out after both closed: {pool.checkedout()}")  # => Output: checked out after both closed: 0
    # => co-18: closing a connection RETURNS it to the pool -- the underlying TCP socket to Postgres often stays open

    with engine.connect() as conn3:  # => co-18: borrows a connection AGAIN, after both prior ones were returned
        pid3 = conn3.execute(text("SELECT pg_backend_pid()")).scalar_one()  # => this connection's backend pid
    print(f"pid3 reused an existing pid: {pid3 in (pid1, pid2)}")  # => Output: pid3 reused an existing pid: True
    assert pid3 in (pid1, pid2)  # => co-18: the pool handed back an EXISTING physical connection, not a freshly-opened one
    # => co-18: which of the two it picked depends on FIFO queue order, an implementation detail -- what matters is
    # => that NO third Postgres backend process was ever spawned; opening a NEW connection costs a TCP handshake
    # => plus authentication on every request, so a pool amortizes that cost across many borrow/return cycles instead
    engine.dispose()  # => co-18: closes every pooled connection -- good hygiene at process shutdown, used here for cleanliness
    print("ex-45 OK")  # => Output: ex-45 OK
