# pyright: strict
# Same strict-typing baseline as every other psycopg example in this topic.
"""Example 78: Serializable Throughput Cost."""

# threading powers the SECOND half of this benchmark (worker_conflicting_
# update) -- the first half deliberately uses NO concurrency, to isolate pure
# per-transaction bookkeeping cost from conflict/retry cost.
import threading
import time

import psycopg

# Every function in this file (setup, both benchmarks) connects to the SAME
# database via this one shared DSN constant.
DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance

TRANSACTION_COUNT = 1000  # => enough repetitions to average out per-connection noise


# A single-row counter, reset before EACH benchmark phase -- this example runs
# THREE separate measurements below, and each needs to start from the same
# known state (value = 0) to be comparable.
def setup() -> None:  # => resets state -- fully self-contained
    # A SINGLE connection for the entire loop below -- no per-iteration
    # connect/close overhead to contaminate the isolation-cost measurement.
    conn = psycopg.connect(DSN)
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        # Idempotent reset, same pattern used throughout this topic.
        cur.execute("DROP TABLE IF EXISTS counter_row CASCADE")
        cur.execute(
            "CREATE TABLE counter_row(id INTEGER PRIMARY KEY, value INTEGER NOT NULL)"
        )
        cur.execute("INSERT INTO counter_row(id, value) VALUES (1, 0)")
    conn.commit()
    conn.close()


# This function's ENTIRE point is what it does NOT do: no threads, no second
# connection, nothing to conflict with -- any timing gap between the two calls
# to this function (once per level) is SSI's own bookkeeping tax, isolated.
def benchmark_isolation_overhead(use_serializable: bool) -> float:
    # => measures SSI's PURE per-transaction bookkeeping cost (co-15) -- a single
    # => connection, NO concurrency, so there is NOTHING to conflict with here --
    # => any timing difference is overhead alone, not conflict/retry cost
    # Each of the 20 concurrent threads gets its OWN separate connection --
    # this models 20 truly independent client sessions racing on one row.
    conn = psycopg.connect(DSN)
    started = time.perf_counter()
    with conn.cursor() as cur:
        for _ in range(TRANSACTION_COUNT):
            # psycopg's execute() requires a LiteralString -- a bool branch
            # keeps each call a true literal instead of an interpolated string.
            if use_serializable:
                cur.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
            else:
                # REPEATABLE READ is the baseline comparison, not READ COMMITTED --
                # both REPEATABLE READ and SERIALIZABLE take a snapshot at BEGIN,
                # so this isolates SSI's EXTRA predicate-locking work specifically.
                cur.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
            # A trivial single-row UPDATE -- cheap enough that 1,000 iterations
            # complete quickly, keeping the WHOLE benchmark fast to run.
            cur.execute("UPDATE counter_row SET value = value + 1 WHERE id = 1")
            conn.commit()
    # elapsed captures the FULL loop duration -- 1,000 BEGIN/UPDATE/COMMIT
    # cycles, timed as a single block for a stable, low-noise average.
    elapsed = time.perf_counter() - started
    conn.close()
    return elapsed


# Unlike the function above, this ONE deliberately creates a genuine conflict:
# every thread reads then writes the SAME row, guaranteeing SSI has real
# dependency cycles to detect and abort, not just paperwork to file.
def worker_conflicting_update(results: list[str]) -> None:
    # => a REAL conflict source: every thread reads THEN writes the SAME row (co-15)
    conn = psycopg.connect(DSN)
    try:
        with conn.cursor() as cur:
            cur.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
            # The read-then-write pattern (read a value, then update based on it)
            # is EXACTLY the shape SSI's dependency tracking watches for.
            cur.execute("SELECT value FROM counter_row WHERE id = 1")
            cur.fetchone()
            cur.execute("UPDATE counter_row SET value = value + 1 WHERE id = 1")
            conn.commit()
            # A successful commit here means this thread's read/write pair did
            # NOT collide with any other thread's dependency at commit time.
            results.append("committed")
    except psycopg.errors.SerializationFailure:
        # No retry loop here (unlike Example 60) -- this benchmark only counts
        # HOW OFTEN a retry would be needed, not what a full retry recovery costs.
        conn.rollback()
        results.append("retry_needed")
    # Always closed, whether the try block succeeded or the except branch ran.
    conn.close()


# main() runs three phases in sequence: (1) REPEATABLE READ baseline overhead,
# (2) SERIALIZABLE baseline overhead, (3) SERIALIZABLE under real concurrent
# contention -- together they separate "cost of the feature" from "cost of
# actually needing it."
def main() -> None:  # => the script's entry point
    setup()
    repeatable_read_seconds = benchmark_isolation_overhead(use_serializable=False)
    setup()
    serializable_seconds = benchmark_isolation_overhead(use_serializable=True)
    # A positive percentage here is SSI's pure bookkeeping tax -- typically
    # small, because with zero contention there is nothing for SSI to actually
    # detect or abort.
    overhead_pct = (serializable_seconds / repeatable_read_seconds - 1) * 100
    print(
        # Printed BEFORE the overhead percentage below -- readers see the raw
        # numbers first, then the derived comparison.
        f"REPEATABLE READ: {TRANSACTION_COUNT} txns in {repeatable_read_seconds:.3f}s"
    )
    print(f"SERIALIZABLE:    {TRANSACTION_COUNT} txns in {serializable_seconds:.3f}s")
    print(f"SSI bookkeeping overhead (no contention): {overhead_pct:.1f}%")

    # This third setup() resets the counter for phase 3 -- the concurrent-conflict
    # measurement below needs its own clean starting state, independent of the
    # 2,000 UPDATEs already run by the two benchmark_isolation_overhead() calls.
    setup()
    results: list[str] = []
    # 20 threads racing on the SAME row -- enough genuine contention that some
    # fraction of them are statistically certain to hit a serialization failure.
    # A list comprehension builds all 20 Thread objects up front, before any
    # of them are started -- this ensures they all begin as close to
    # simultaneously as possible on the next loop below.
    threads = [
        threading.Thread(target=worker_conflicting_update, args=(results,))
        for _ in range(20)
    ]
    # Starting all threads first, in a separate loop from joining them, is
    # what maximizes the actual overlap window between their transactions.
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # results is populated by all 20 threads independently -- counting after
    # every t.join() above guarantees every append() has already happened.
    retry_count = results.count("retry_needed")
    print(
        f"Concurrent conflicting workers: {len(results)} total, {retry_count} needed retry"
    )
    # => under REAL contention, a nonzero fraction of SERIALIZABLE transactions
    # => abort with SerializationFailure and MUST be retried (co-15) -- the price
    # => correctness costs under genuine concurrent conflict, not just bookkeeping


# The overall lesson: SSI's raw per-transaction overhead is usually modest, but
# a WORKLOAD with genuine contention must budget for a nonzero retry rate --
# design the application's retry logic (Example 60) accordingly.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
