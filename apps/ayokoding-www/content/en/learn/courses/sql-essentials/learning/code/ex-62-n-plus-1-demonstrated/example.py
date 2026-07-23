# pyright: strict
"""Example 62: N+1 Query Problem Demonstrated."""

import sqlite3  # => stdlib DB-API module (co-19) -- no third-party driver needed


def setup(conn: sqlite3.Connection) -> None:
    # A fresh in-memory schema + seed data -- this example needs NO leftover state (self-contained).
    conn.executescript(
        """
        -- a minimal parent table -- just enough to demonstrate the per-parent loop below
        CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);  -- 1 parent table
        -- author_id is NOT a foreign key here -- the point is the QUERY PATTERN, not the schema
        CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL);
        -- 2 authors -- Ada will end up with 2 books below, Grace with 1
        INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace'), (2, 'Grace Hopper');  -- 2 rows
        -- 3 books total, split 2-and-1 across the 2 authors above
        INSERT INTO book(id, title, author_id) VALUES  -- a 3-row multi-VALUES insert
            (1, 'Notes on the Analytical Engine', 1),  -- Ada's first book
            (2, 'Sketch of the Analytical Engine', 1),  -- Ada's second book
            (3, 'The First Computer Bug', 2);  -- Grace's only book
        """
    )  # => author has 2 rows, book has 3 rows -- 2 belong to author 1, 1 belongs to author 2
    conn.commit()  # => persists the schema + seed data before any reporting query runs


def main() -> (
    None
):  # => the entry point -- runs setup(), then the N+1 loop, then a summary
    conn: sqlite3.Connection = sqlite3.connect(
        ":memory:"
    )  # => a throwaway, process-local DB
    setup(conn)  # => builds the 2-author, 3-book fixture this whole example reads from

    query_count: int = 0  # => a manual counter -- makes the "N+1" round trips VISIBLE
    authors: list[tuple[int, str]] = (
        conn.execute(  # => query #1, below -- the parent fetch
            "SELECT id, name FROM author"  # => no WHERE -- every author row, unconditionally
        ).fetchall()
    )  # => drains the cursor into a plain Python list right away
    # => fetchall() drains the cursor into a plain list -- 2 rows, one PER author
    query_count += 1  # => query #1 -- fetches every parent (author) row, once

    results: list[
        tuple[str, list[str]]
    ] = []  # => accumulates (author_name, titles) pairs
    for (
        author_id,
        author_name,
    ) in authors:  # => THIS loop is the anti-pattern -- N iterations
        # A SEPARATE round trip to the engine, PER author -- the "N" in "N+1" (co-23).
        titles_cur: sqlite3.Cursor = conn.execute(  # => opens a FRESH cursor every iteration
            "SELECT title FROM book WHERE author_id = ?",  # => filters to ONE author per call
            (author_id,),  # => the single bound parameter for THIS iteration
        )  # => runs a fresh query EVERY time the loop body executes
        titles: list[str] = [
            row[0] for row in titles_cur.fetchall()
        ]  # => unwraps 1-tuples
        query_count += 1  # => tallies each per-author query as it fires
        results.append(
            (author_name, titles)
        )  # => appends this author's (name, titles) pair

    for (
        name,
        titles,
    ) in results:  # => a SEPARATE loop -- just prints what was already fetched
        print(
            name, titles
        )  # => Output: one line per author, its titles as a Python list
    print(
        f"queries executed: {query_count}"
    )  # => 1 + 2 = 3 total -- co-23's cost, made visible
    conn.close()  # => releases the in-memory connection -- nothing to clean up on disk


if __name__ == "__main__":  # => guards main() so importing this module never runs it
    main()  # => runs the whole demonstration end to end
