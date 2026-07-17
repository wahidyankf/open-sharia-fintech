# pyright: strict
# Same strict-typing baseline as every other psycopg example in this topic --
# psycopg_pool ships its own type stubs alongside psycopg's.
"""Example 76: Connection Pooling Benchmark."""

import time

import psycopg
from psycopg.rows import TupleRow

# ConnectionPool is a SEPARATE package from core psycopg -- pooling is an
# opt-in add-on, not baked into every psycopg connection by default.
from psycopg_pool import ConnectionPool

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance

REQUEST_COUNT = 300  # => simulates 300 short-lived "requests," each running 1 query


# Both benchmark functions run the IDENTICAL query (SELECT 1) the SAME number
# of times -- the only variable being measured is HOW each connection is
# obtained, isolating connection overhead as the one thing this example teaches.
def benchmark_per_request_connection() -> float:
    # => the NAIVE pattern: open a BRAND NEW TCP connection + auth handshake for
    # => every single request, then throw it away (co-28) -- common in code that
    # => forgets connection pooling, or in naive serverless-function handlers
    started = time.perf_counter()
    for _ in range(REQUEST_COUNT):
        # Each iteration pays the FULL cost: TCP handshake, PostgreSQL
        # authentication, and backend process fork -- then discards all of it.
        conn = psycopg.connect(DSN)
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        conn.close()
    return time.perf_counter() - started


# psycopg.Connection[TupleRow] is the generic type parameter that tells pyright
# exactly what row shape fetchone()/fetchall() will return -- without it, the
# pool's connection type would be only partially known under strict mode.
def benchmark_pooled_connection(
    pool: ConnectionPool[psycopg.Connection[TupleRow]],
) -> float:
    # => the FIX (co-28): a pool keeps a small set of connections ALREADY open and
    # => authenticated -- "borrowing" one costs almost nothing compared to a fresh
    # => TCP handshake + PostgreSQL's own authentication + backend process startup
    started = time.perf_counter()
    for _ in range(REQUEST_COUNT):
        # pool.connection() is a context manager -- it hands back an ALREADY-OPEN
        # connection and automatically returns it to the pool when the block exits,
        # rather than closing the underlying TCP connection at all.
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
    return time.perf_counter() - started


# main() runs both benchmarks back to back and reports the speedup ratio --
# the exact numbers vary by machine, but the pooled version is consistently
# an order of magnitude faster for this many short-lived requests.
def main() -> None:  # => the script's entry point
    per_request_seconds = benchmark_per_request_connection()
    print(
        f"Per-request connections: {REQUEST_COUNT} requests in {per_request_seconds:.3f}s"
    )
    # => Output: Per-request connections: 300 requests in 1.536s (each pays full connect cost)

    # min_size=4, max_size=4 creates a FIXED pool of 4 connections -- enough to
    # serve REQUEST_COUNT sequential requests without ever needing to grow.
    with ConnectionPool[psycopg.Connection[TupleRow]](
        DSN, min_size=4, max_size=4
    ) as pool:
        pool.wait()  # => blocks until the pool's minimum connections are actually open and ready
        pooled_seconds = benchmark_pooled_connection(pool)
        print(f"Pooled connections: {REQUEST_COUNT} requests in {pooled_seconds:.3f}s")
        # => Output: Pooled connections: 300 requests in 0.169s -- roughly an order of magnitude faster

    # The `with` block above closes the pool cleanly BEFORE this ratio is
    # computed -- pooled_seconds is already captured, so closing has no effect on it.
    speedup = per_request_seconds / pooled_seconds
    print(f"Speedup: {speedup:.1f}x")


# In production, pool.wait() at startup is optional but recommended -- without
# it, the FIRST few requests after the process starts would pay a partial
# connect cost while the pool lazily opens, connects, and adds each of its 4
# minimum connections one at a time, on demand, instead of paying that setup
# cost upfront before any request arrives.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
