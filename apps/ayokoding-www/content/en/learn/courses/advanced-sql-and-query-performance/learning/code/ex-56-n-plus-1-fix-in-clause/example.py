# pyright: strict
# Same strict-typing setup as Examples 54-55 -- psycopg's own stubs cover
# every DB-API call here without any extra typing scaffolding.
"""Example 56: N+1 Fix, IN Clause."""

import time

# time is the only extra import beyond psycopg -- this fix needs no additional
# library support, just a different query shape and one in-memory dict.
import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


# The THIRD identical copy of this setup() (see Examples 54 and 55) -- three
# scripts sharing one dataset is what makes their elapsed-time numbers a fair
# three-way comparison of N+1, JOIN, and batched-IN strategies.
def setup(conn: psycopg.Connection) -> None:  # => resets state -- fully self-contained
    """Create the SAME author/book shape as Examples 54-55, for a fair comparison."""
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        cur.execute("DROP TABLE IF EXISTS book, author CASCADE")
        cur.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        # The FK still guarantees every book has a real author_id to look up -- no
        # NULL/missing-author edge case for the batched query below to special-case.
        cur.execute(
            "CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, "
            "author_id INTEGER NOT NULL REFERENCES author(id))"
        )
        # Same 500-author seed as Examples 54-55 -- ids 1 through 500, sequential,
        # no gaps.
        cur.execute(
            "INSERT INTO author(id, name) SELECT n, 'Author ' || n "
            "FROM generate_series(1, 500) AS n"
        )
        # Same 1 + (n % 500) author_id cycling as Examples 54-55 -- 500 books, one
        # per author, identical dataset shape across all three N+1 scripts.
        cur.execute(
            "INSERT INTO book(id, title, author_id) "
            "SELECT n, 'Book ' || n, 1 + (n % 500) FROM generate_series(1, 500) AS n"
        )
    conn.commit()


# main() demonstrates the SECOND fix strategy: batch every needed author_id
# into ONE query via ANY(...), rather than Example 55's JOIN or Example 54's
# one-query-per-row loop.
def main() -> None:  # => the script's entry point
    conn = psycopg.connect(DSN)
    setup(conn)

    # Timing again starts after setup() completes, matching Examples 54 and 55's
    # measurement boundary exactly.
    started = time.perf_counter()
    with conn.cursor() as outer:
        # Identical first query to Example 54's N+1 version -- fetch every book in
        # ONE round trip; the difference between all three scripts is entirely in
        # what happens NEXT.
        outer.execute("SELECT id, title, author_id FROM book ORDER BY id")
        books = outer.fetchall()
        # => 1 query for all books -- same starting point as Example 54's N+1 version
        # A set comprehension deduplicates author_ids BEFORE the query runs -- with
        # only 500 authors shared across 500 books there is no duplication here, but
        # a more skewed dataset (many books per author) would make this dedup step
        # essential for keeping the batched query small.
        author_ids = list({row[2] for row in books})
        # => collect the DISTINCT author_ids needed -- a set, so duplicates cost nothing
        with conn.cursor() as inner:
            # => the FIX (co-26): ONE batched query using ANY(%s) with a Python list
            # => param -- fetches every needed author row in a SINGLE round trip
            # ANY(%s) with a Python list parameter is psycopg's idiom for a parameterized
            # IN-list -- it avoids building a dynamic SQL string with one placeholder per
            # id, which would need to change shape based on how many ids happen to exist.
            inner.execute(
                "SELECT id, name FROM author WHERE id = ANY(%s)", (author_ids,)
            )
            # dict(...) over a list of (id, name) 2-tuples is a direct, idiomatic way to
            # turn a fetched result set into an id-keyed lookup table.
            authors = dict(inner.fetchall())
            # => an in-memory dict for O(1) local lookups -- no further database calls
        # This loop iterates the SAME 500 books as Example 54's version -- the
        # difference is that every author_id lookup below is now a local dict access,
        # not a fresh database round trip.
        for _book_id, _title, author_id in books:
            # The lookup result is not stored anywhere -- this loop exists purely to
            # prove every book's author IS present in the dict, with zero further queries.
            authors[author_id]
            # => local dict lookup, zero network cost -- this is where the win pays off
    elapsed = time.perf_counter() - started
    print(f"IN-clause fix: {len(books)} books, 2 total queries")
    # => Output: IN-clause fix: 500 books, 2 total queries
    print(f"Elapsed: {elapsed:.3f}s")
    # => Output: Elapsed: 0.002s (captured) -- comparable to Example 55's JOIN fix

    # One connection, one close() -- identical resource-cleanup shape to
    # Examples 54 and 55.
    conn.close()  # => always close what you open


# Compare this script's "2 total queries" against Example 54's 501 and
# Example 55's 1 -- three different trade-offs for solving the identical
# N+1 problem.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
