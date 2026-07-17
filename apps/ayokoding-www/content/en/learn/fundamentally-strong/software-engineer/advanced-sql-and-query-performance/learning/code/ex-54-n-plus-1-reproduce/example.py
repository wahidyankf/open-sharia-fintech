# pyright: strict
# psycopg's native type stubs let pyright resolve every DB-API call below
# to a concrete type -- no third-party stub package or Any fallback needed.
"""Example 54: N+1 Reproduce."""

# time.perf_counter() (used below) is the standard-library choice for measuring
# short wall-clock durations -- monotonic, unaffected by system clock adjustments.
import time

import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance
# A single connection is enough here -- unlike Examples 26/27, this script
# demonstrates a WITHIN-one-session performance anti-pattern, not cross-session
# concurrency.


# setup() seeds a 1:1 author-to-book ratio (500 authors, 500 books) --
# deliberately the WORST case for N+1: every single book row needs its own
# separate author lookup, none of which can be batched or reused.
def setup(conn: psycopg.Connection) -> None:  # => resets state -- fully self-contained
    """Create an author/book pair sized to make N+1 overhead visible."""
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        cur.execute("DROP TABLE IF EXISTS book, author CASCADE")
        cur.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        # author_id is NOT NULL -- every book is guaranteed to trigger exactly one
        # inner lookup below, with no NULL-author edge case to complicate the count.
        cur.execute(
            "CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, "
            "author_id INTEGER NOT NULL REFERENCES author(id))"
        )
        # String literals are split across two lines here purely for line-length --
        # Postgres and psycopg both see this as ONE ordinary SQL statement string.
        cur.execute(
            "INSERT INTO author(id, name) SELECT n, 'Author ' || n "
            "FROM generate_series(1, 500) AS n"
        )
        # 1 + (n % 500) cycles author_id through 1..500 in lockstep with book's own
        # n -- guaranteeing the promised 1 book per author, no author left un-referenced.
        cur.execute(
            "INSERT INTO book(id, title, author_id) "
            "SELECT n, 'Book ' || n, 1 + (n % 500) FROM generate_series(1, 500) AS n"
        )
        # => 500 authors, 500 books -- one book per author (co-26): worst case for N+1
    conn.commit()


# main() times ONLY the query-execution portion of the N+1 pattern -- setup()
# and connection handling run and complete before the perf_counter() clock starts.
def main() -> None:  # => the script's entry point
    conn = psycopg.connect(DSN)
    setup(conn)

    # Capturing the start time AFTER setup() completes isolates what this example
    # actually wants to measure: the cost of the N+1 QUERY pattern itself.
    started = time.perf_counter()
    with conn.cursor() as outer:
        # ORDER BY id makes book iteration order deterministic -- irrelevant to
        # correctness here, but it keeps repeated runs directly comparable.
        outer.execute("SELECT id, title, author_id FROM book ORDER BY id")
        books = outer.fetchall()
        # => 1 query for all books -- looks efficient so far
        # Leading underscores on _book_id/_title signal "deliberately unused" -- only
        # author_id is needed to drive the inner per-row lookup below; pyright --strict
        # would otherwise flag genuinely unused bindings depending on lint configuration.
        for _book_id, _title, author_id in books:
            # Opening a FRESH cursor per iteration (rather than reusing one) mirrors how
            # many ORMs implement lazy-loaded relationships -- one new cursor/statement per
            # accessed related object, which is the crux of the N+1 anti-pattern.
            with conn.cursor() as inner:
                # => N+1 (co-26): a SEPARATE round trip to the server for EVERY row
                # => above -- 500 extra queries, each paying full network + parse cost
                # %s with a separate parameter tuple is psycopg's parameterized-query syntax --
                # it prevents SQL injection and lets Postgres reuse a cached query plan across
                # calls, but does NOT reduce the round-trip COUNT this example is measuring.
                inner.execute("SELECT name FROM author WHERE id = %s", (author_id,))
                inner.fetchone()
    # Elapsed time here includes 501 total network round trips: 1 for the book
    # list plus 500 individual author lookups, each paying its own latency.
    elapsed = time.perf_counter() - started
    print(f"N+1 pattern: {len(books)} books, {len(books) + 1} total queries")
    # => Output: N+1 pattern: 500 books, 501 total queries
    print(f"Elapsed: {elapsed:.3f}s")
    # => Output: Elapsed: 0.106s (captured; absolute timing is machine-dependent)

    # A single connection.close() is sufficient -- every cursor above was already
    # closed automatically by its own `with` block on exit.
    conn.close()  # => always close what you open


# Example 55 and 56 both fix this exact N+1 pattern -- one via a JOIN, one via
# a single IN (...) batched lookup -- reusing this SAME schema and seed data.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
