# pyright: strict
"""Example 47: pool_pre_ping -- Transparently Recovering a Stale Pooled Connection."""

from __future__ import annotations

import os  # => reads connection settings from the environment

import psycopg  # => co-18: a RAW driver connection for the killer -- must be a DIFFERENT physical backend than the pool's
from sqlalchemy import Engine, create_engine, text  # => co-18: pool_pre_ping is a create_engine() keyword, not a pool method
from sqlalchemy.exc import OperationalError  # => co-18: what a STALE connection raises WITHOUT pre-ping's protection

PG_DSN: str = os.environ.get("PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example")  # => a plain DB-API DSN
SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


def make_stale(engine: Engine) -> None:  # => borrows the pool's connection, notes its pid, then kills it FROM OUTSIDE the pool
    with engine.connect() as conn:  # => co-18: checks out the pool's connection -- this becomes the STALE one once returned
        pid = conn.execute(text("SELECT pg_backend_pid()")).scalar_one()  # => Postgres' own process id for THIS connection
    with psycopg.connect(PG_DSN, autocommit=True) as killer:  # => a connection OUTSIDE the pool -- can't kill itself by accident
        killer.execute("SELECT pg_terminate_backend(%s)", (pid,))  # => forcibly kills the pool's connection, not this one
    # => co-18: the pool does NOT know yet -- `conn`'s connection object is back in the pool, looking perfectly healthy


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    no_ping_engine = create_engine(SQLA_URL, pool_size=1, max_overflow=0)  # => co-18: pool_pre_ping DEFAULTS to False
    make_stale(no_ping_engine)  # => kills the pool's one connection behind its back
    try:  # => the pool hands back the connection it THINKS is fine -- it never verified
        with no_ping_engine.connect() as conn:  # => co-18: reuses the now-DEAD connection, no health check first
            conn.execute(text("SELECT 1"))  # => this round trip fails -- Postgres already closed the socket
        raise AssertionError("expected OperationalError")  # => fails loudly if the connection was somehow still alive
    except OperationalError as exc:  # => co-18: without pre-ping, staleness surfaces as a hard failure on the CALLER's query
        print(f"no pre_ping raised: {type(exc).__name__}")  # => Output: no pre_ping raised: OperationalError
    no_ping_engine.dispose()  # => closes every pooled connection -- good hygiene before building the next engine

    ping_engine = create_engine(SQLA_URL, pool_size=1, max_overflow=0, pool_pre_ping=True)  # => co-18: the protection ENABLED
    make_stale(ping_engine)  # => kills THIS pool's one connection behind its back, identically to the run above
    with ping_engine.connect() as conn:  # => co-18: pre_ping runs a lightweight "SELECT 1" BEFORE handing this out
        result = conn.execute(text("SELECT 1")).scalar_one()  # => co-18: succeeds -- pre-ping silently opened a FRESH connection
        print(f"with pre_ping result: {result}")  # => Output: with pre_ping result: 1
        assert result == 1  # => co-18: the caller never even sees the staleness -- pre-ping absorbed it transparently
    # => co-18: pool_pre_ping adds one extra round trip PER checkout, a small, worthwhile cost for connections that
    # => might have gone stale behind a load balancer, a database failover, or a long idle period -- exactly the
    # => class of production incident ("connection reset" errors after a quiet night) this setting quietly prevents
    ping_engine.dispose()  # => closes every pooled connection -- good hygiene at process shutdown, used here for cleanliness
    print("ex-47 OK")  # => Output: ex-47 OK
