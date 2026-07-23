# pyright: strict
# Same strict-typing baseline as every other psycopg example in this topic.
"""Example 75: Materialized View, CONCURRENTLY."""

# threading and time together let this example PROVE readers are never
# blocked, by racing a background refresh against a foreground read.
import threading
import time

import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


# Two prerequisites must both be satisfied before REFRESH ... CONCURRENTLY can
# be used at all -- setup() establishes both, so main() can focus purely on
# demonstrating the concurrent-refresh behavior itself.
def setup() -> None:  # => resets state -- fully self-contained
    """Seed a large base table and populate the materialized view NON-concurrently."""
    conn = psycopg.connect(DSN)
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        # The materialized view is dropped BEFORE its base table, same FK-safety
        # ordering used in Example 64.
        cur.execute("DROP MATERIALIZED VIEW IF EXISTS sale_summary_mv CASCADE")
        # Idempotent reset, same pattern used throughout this topic.
        cur.execute("DROP TABLE IF EXISTS sale_row_big CASCADE")
        cur.execute(
            "CREATE TABLE sale_row_big(id INTEGER PRIMARY KEY, category TEXT NOT NULL, "
            # category is a plain TEXT computed from n % 50 -- amount uses
            # NUMERIC(10,2) for exact money math, matching this topic's convention.
            "amount NUMERIC(10,2) NOT NULL)"
        )
        # 50 distinct categories, spread across 3 million rows -- enough real
        # aggregation work per category that the refresh takes a measurable amount
        # of time, which is exactly what this example needs to race against.
        cur.execute(
            "INSERT INTO sale_row_big(id, category, amount) "
            "SELECT n, 'cat-' || (n % 50), (10 + (n % 90))::NUMERIC "
            "FROM generate_series(1, 3000000) AS n"
        )
        # => 3,000,000 rows -- large enough that the refresh below takes long enough
        # => to genuinely OVERLAP with a concurrent read (co-27)
        cur.execute(
            "CREATE MATERIALIZED VIEW sale_summary_mv AS "
            "SELECT category, SUM(amount) AS total_amount, COUNT(*) AS sale_count "
            "FROM sale_row_big GROUP BY category"
        )
        # => the FIRST population must be a regular (non-concurrent) CREATE/REFRESH --
        # => REFRESH ... CONCURRENTLY requires the view to ALREADY hold data (co-27 prerequisite #1)
        cur.execute(
            "CREATE UNIQUE INDEX idx_sale_summary_mv_category ON sale_summary_mv(category)"
        )
        # => a plain UNIQUE index on the view is REQUIRED before CONCURRENTLY works at
        # => all (co-27 prerequisite #2) -- it is how PostgreSQL diffs old vs new rows
    # A single commit covers the base table seed, the initial materialized
    # view population, and the unique index -- all part of one setup transaction.
    conn.commit()
    conn.close()


# This function runs on a dedicated background thread (see main()) so its
# REFRESH can genuinely overlap in time with the read happening concurrently
# on a completely separate connection.
def run_refresh_concurrently(timings: dict[str, float]) -> None:
    # => runs on its OWN connection, in its OWN thread -- REFRESH ... CONCURRENTLY
    # => takes only a ROW-level lock internally, unlike Example 64's plain REFRESH
    conn = psycopg.connect(DSN)
    # Without autocommit=True, psycopg wraps every statement in an implicit
    # transaction block -- and CONCURRENTLY explicitly forbids running inside one.
    conn.autocommit = True  # => REFRESH CONCURRENTLY cannot run inside a multi-statement transaction block
    started = time.perf_counter()
    with conn.cursor() as cur:
        # This single statement is where all the work happens -- it recomputes
        # the view's query in the background while old rows stay fully readable.
        cur.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY sale_summary_mv")
    timings["refresh_seconds"] = time.perf_counter() - started
    conn.close()


# main() launches the refresh on a background thread, then immediately tries
# to read from the SAME materialized view on the main thread -- if
# CONCURRENTLY truly avoids blocking, that read should return almost instantly.
def main() -> None:  # => the script's entry point
    setup()
    # A plain dict passed by reference into the background thread -- Python's
    # GIL makes this single-key write/read safe without an explicit lock here.
    timings: dict[str, float] = {}
    refresh_thread = threading.Thread(target=run_refresh_concurrently, args=(timings,))
    refresh_thread.start()
    # 20ms is small relative to a multi-million-row refresh but large enough
    # for the background thread to have genuinely started its REFRESH statement.
    time.sleep(
        0.02
    )  # => a brief head start -- ensures the refresh is genuinely IN FLIGHT
    # => before the read below fires, so the read has something to race against

    # A SEPARATE connection for the read -- this models a genuinely different
    # client/request, not just a different statement on the refresh's own connection.
    read_conn = psycopg.connect(DSN)
    read_started = time.perf_counter()
    with read_conn.cursor() as cur:
        # A trivial COUNT(*) against the small (50-row) summary view -- this
        # is deliberately cheap so any slowness observed comes from BLOCKING,
        # not from the read query's own cost.
        cur.execute("SELECT COUNT(*) FROM sale_summary_mv")
        cur.fetchone()
    read_elapsed = time.perf_counter() - read_started
    # Closing the read connection immediately after use -- it has no further
    # role once its single COUNT(*) has been timed and discarded.
    read_conn.close()

    # join() waits for the background refresh to fully finish before printing
    # timings['refresh_seconds'] -- otherwise that key might not exist yet.
    refresh_thread.join()
    print(f"Concurrent read elapsed: {read_elapsed:.4f}s")
    # Printing both elapsed times side by side makes the contrast concrete --
    # readers can see the read completing in a fraction of the refresh's duration.
    print(f"REFRESH CONCURRENTLY total elapsed: {timings['refresh_seconds']:.4f}s")
    # => the READ finishes in milliseconds, while the REFRESH is still running in the
    # => background for much longer -- proving readers were NEVER blocked (co-27),
    # => unlike Example 64's plain REFRESH, which would have made this read WAIT


# The cost of CONCURRENTLY is not free -- it requires a unique index, runs
# roughly twice as much work internally (a full recompute PLUS a row-by-row
# diff against the old data), and takes longer wall-clock time than a plain
# REFRESH would for the same view.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
