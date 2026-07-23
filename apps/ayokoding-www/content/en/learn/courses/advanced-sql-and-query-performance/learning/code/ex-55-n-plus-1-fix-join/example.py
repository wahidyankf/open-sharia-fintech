# pyright: strict
# Same psycopg strict-typing setup as Example 54 -- only main()'s query strategy
# differs between the two files.
"""Example 55: N+1 Fix, JOIN."""

import time

# No new imports beyond Example 54's time and psycopg -- the fix needs no
# additional library support, just a different SQL statement.
import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance
# One connection is all the FIXED version needs too -- the fix is about QUERY
# shape, not about connection or session strategy.


# Byte-for-byte the SAME setup() as Example 54 -- an identical dataset is what
# makes the elapsed-time comparison between the two scripts meaningful.
def setup(conn: psycopg.Connection) -> None:  # => resets state -- fully self-contained
    """Create the SAME author/book shape as Example 54, for a fair comparison."""
    # Same cursor-per-call pattern as every earlier psycopg example in this topic --
    # see Example 26 for the underlying context-manager mechanics.
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        # Resetting both tables guarantees this script's 500/500 row counts and its
        # elapsed-time comparison against Example 54 both start from identical state.
        cur.execute("DROP TABLE IF EXISTS book, author CASCADE")
        cur.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        # Every book row again has a NOT NULL author_id -- the JOIN below can rely on
        # finding a matching author for each and every book, no OUTER join needed.
        cur.execute(
            "CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, "
            "author_id INTEGER NOT NULL REFERENCES author(id))"
        )
        # Author rows are seeded identically to Example 54 -- 500 authors, sequential
        # ids -- so the JOIN below has exactly one matching author per book, always.
        cur.execute(
            "INSERT INTO author(id, name) SELECT n, 'Author ' || n "
            "FROM generate_series(1, 500) AS n"
        )
        # Same 1 + (n % 500) cycling as Example 54 -- every book maps to exactly one
        # of the 500 authors, with no book left unmatched.
        cur.execute(
            "INSERT INTO book(id, title, author_id) "
            "SELECT n, 'Book ' || n, 1 + (n % 500) FROM generate_series(1, 500) AS n"
        )
    # Committing here makes the seeded rows visible to the SAME connection's next
    # statement -- unlike Examples 26/27, there is only one session in play, so
    # this commit is about durability/visibility bookkeeping, not cross-session concurrency.
    conn.commit()


# main() runs the FIXED query strategy: one JOIN instead of one query-per-row
# -- everything else (setup, timing harness, print format) mirrors Example 54
# closely enough that the elapsed-time numbers are directly comparable.
def main() -> None:  # => the script's entry point
    # A single connect() call -- Example 54 also used just one connection, since
    # N+1 is a WITHIN-session anti-pattern, not a multi-session one.
    conn = psycopg.connect(DSN)
    # setup(conn) is called once, exactly as in Example 54, before any timing
    # begins.
    setup(conn)

    # Timing starts after setup(), exactly as in Example 54 -- so both scripts
    # measure only their OWN query-execution strategy, not connection/seed overhead.
    started = time.perf_counter()
    with conn.cursor() as cur:
        # => the FIX (co-26): pull book + author together in ONE query via JOIN --
        # => the database does the row-matching work it is built for, in one pass
        # JOIN ON a.id = b.author_id is the ordinary equi-join pattern used throughout
        # this topic's SQL examples -- the fix here is entirely about NOT issuing a
        # separate query per book, not about any exotic join syntax.
        cur.execute(
            "SELECT b.id, b.title, a.name FROM book b JOIN author a ON a.id = b.author_id "
            "ORDER BY b.id"
        )
        # fetchall() materializes the ENTIRE joined result set in one call -- the
        # server did the row-matching; the client just receives the finished rows.
        rows = cur.fetchall()
        # => exactly 1 round trip total, vs 501 in Example 54's N+1 version
    elapsed = time.perf_counter() - started
    print(f"JOIN fix: {len(rows)} books, 1 total query")
    # => Output: JOIN fix: 500 books, 1 total query
    print(f"Elapsed: {elapsed:.3f}s")
    # => Output: Elapsed: 0.001s (captured) -- roughly two orders of magnitude faster
    # Both this fixed version's elapsed time and Example 54's are captured on the
    # same class of hardware -- the RELATIVE gap between them is the point, not
    # either absolute number in isolation.

    conn.close()  # => always close what you open


# Run Example 54 and this file back to back to see the elapsed-time gap
# directly -- same data, same result set, radically different round-trip count.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
