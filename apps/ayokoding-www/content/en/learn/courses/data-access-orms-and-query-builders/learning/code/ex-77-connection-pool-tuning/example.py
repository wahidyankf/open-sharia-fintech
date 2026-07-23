# pyright: strict
"""Example 77: Tuning the Pool for a Concurrency Target -- Measured Throughput, Not a Guess."""

from __future__ import annotations

import os  # => reads connection settings from the environment
import time  # => wall-clock timing -- the measured evidence, not an assumed claim
from concurrent.futures import ThreadPoolExecutor  # => co-18: real concurrent WORKERS, each needing its own pooled connection

from sqlalchemy import Engine, create_engine, select, text  # => co-18: pool_size/max_overflow are create_engine() keywords
from sqlalchemy.orm import Session  # => a Session is the ORM's unit-of-work handle, one per worker below

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


def worker(engine: Engine) -> None:  # => co-18: ONE simulated request -- checks out a connection, does 0.2s of DB work, returns it
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        session.execute(select(text("pg_sleep(0.2)")))  # => co-18: simulates a slow query -- 0.2s of server-side wait, per worker


def run_workload(engine: Engine, n_workers: int) -> float:  # => co-18: launches n_workers CONCURRENT requests, times the batch
    start = time.monotonic()  # => wall-clock start, right before the concurrent workers launch
    with ThreadPoolExecutor(max_workers=n_workers) as pool:  # => co-18: n_workers THREADS, each wanting a connection AT THE SAME TIME
        futures = [pool.submit(worker, engine) for _ in range(n_workers)]  # => co-18: fires ALL workers concurrently, not one-by-one
        for future in futures:  # => waits for every worker to finish before measuring elapsed time
            future.result()  # => re-raises any worker exception -- a silent failure would corrupt the timing measurement
    return time.monotonic() - start  # => co-18: total wall-clock time for the WHOLE concurrent batch


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    n_workers = 8  # => co-18: the CONCURRENCY TARGET this example tunes the pool for -- 8 simultaneous requests

    undersized_engine = create_engine(SQLA_URL, pool_size=2, max_overflow=0)  # => co-18: WAY below the target -- only 2 connections
    undersized_seconds = run_workload(undersized_engine, n_workers)  # => co-18: 8 workers competing for just 2 connections
    undersized_engine.dispose()  # => closes every pooled connection -- good hygiene before building the next engine

    tuned_engine = create_engine(SQLA_URL, pool_size=n_workers, max_overflow=0)  # => co-18: sized to MATCH the concurrency target
    tuned_seconds = run_workload(tuned_engine, n_workers)  # => co-18: 8 workers, 8 connections -- no queueing for a free one
    tuned_engine.dispose()  # => closes every pooled connection -- good hygiene at process shutdown

    print(f"undersized: {undersized_seconds:.2f}s")  # => Output: undersized: <around 0.80s, varies by machine>
    print(f"tuned: {tuned_seconds:.2f}s")  # => Output: tuned: <around 0.20s, varies by machine>
    print(f"tuned faster: {tuned_seconds < undersized_seconds}")  # => Output: tuned faster: True
    assert tuned_seconds < undersized_seconds  # => co-18: the correctly-sized pool measurably beats the undersized one
    assert tuned_seconds < 0.5  # => co-18: 8 workers x 0.2s should overlap into roughly ONE 0.2s window, not stack up serially
    # => co-18: with pool_size=2, 8 workers queue in batches of 2 -- roughly FOUR sequential 0.2s waves, ~0.8s total;
    # => with pool_size=8, all EIGHT workers get a connection immediately and their 0.2s waits overlap into ONE
    # => window, ~0.2s total -- the pool size is a REAL throughput ceiling under concurrency, not a cosmetic setting
    print("ex-77 OK")  # => Output: ex-77 OK
