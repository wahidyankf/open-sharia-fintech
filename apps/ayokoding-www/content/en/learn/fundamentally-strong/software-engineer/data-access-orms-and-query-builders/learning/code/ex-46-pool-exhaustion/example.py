# pyright: strict
"""Example 46: Pool Exhaustion -- QueuePool Times Out When Every Connection Is Held."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import create_engine, text  # => co-18: the engine whose small pool this example deliberately exhausts
from sqlalchemy.exc import TimeoutError as SATimeoutError  # => co-18: renamed to avoid shadowing the builtin TimeoutError

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance

if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(  # => co-18: a DELIBERATELY tiny pool -- easy to exhaust for this demonstration
        SQLA_URL,
        pool_size=1,  # => at most ONE persistent connection
        max_overflow=0,  # => co-18: zero overflow -- no temporary extra connections allowed beyond pool_size
        pool_timeout=1,  # => co-18: how long a checkout WAITS for a free connection before giving up, in seconds
    )

    held_conn = engine.connect()  # => co-18: checks out the pool's ONLY connection and does NOT return it -- held open
    # => this simulates a real hazard: a request that forgets to close its connection, or one that runs unusually long
    try:  # => the checkout below has nowhere to come from -- pool_size=1 is already fully checked out
        try:  # => attempts a SECOND checkout while the first is still held
            engine.connect()  # => co-18: blocks up to pool_timeout seconds, then raises -- there is no connection to give
            raise AssertionError("expected TimeoutError")  # => fails loudly if the pool unexpectedly had room
        except SATimeoutError as exc:  # => co-18: the exact exception QueuePool raises once pool_timeout elapses
            print(f"raised: {type(exc).__name__}")  # => Output: raised: TimeoutError
            # => co-18: the message names QueuePool explicitly -- "QueuePool limit of size 1 overflow 0 reached"
    finally:  # => always releases the held connection, even if the assertion above somehow fired
        held_conn.close()  # => co-18: returns the connection to the pool -- the NEXT checkout would now succeed instantly

    with engine.connect() as conn_after:  # => co-18: proves the pool RECOVERS once a connection is returned
        result = conn_after.execute(text("SELECT 1")).scalar_one()  # => a trivial round trip, just to prove the pool works
        print(f"result after recovery: {result}")  # => Output: result after recovery: 1
        assert result == 1  # => co-18: exhaustion is TEMPORARY -- the pool is healthy again as soon as a slot frees up
    # => co-18: pool_timeout is a deliberate design choice, not a bug -- it turns "every connection is busy" into a
    # => bounded, catchable wait instead of an indefinitely hanging request; a real service sizes pool_size + max_overflow
    # => to its expected concurrent load, and treats a TimeoutError here as a signal to scale the pool or the database
    engine.dispose()  # => closes every pooled connection -- good hygiene at process shutdown, used here for cleanliness
    print("ex-46 OK")  # => Output: ex-46 OK
