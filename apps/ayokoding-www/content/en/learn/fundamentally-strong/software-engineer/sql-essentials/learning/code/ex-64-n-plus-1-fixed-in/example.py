# pyright: strict
"""Example 64: N+1 Fixed with a Batched IN(...) Fetch."""

import sqlite3  # => stdlib DB-API module (co-19)


def setup(conn: sqlite3.Connection) -> None:
    # Same schema and seed data as Examples 62-63 -- a third way to fix the identical problem.
    conn.executescript(
        """
        -- same fixture shape as Examples 62-63 -- comparing a THIRD fix to the identical problem
        CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);  -- 1 parent table
        CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL);
        -- author_id is a plain integer column here too -- the fix is a SECOND batched query
        -- 2 authors, exactly as in Examples 62-63
        INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace'), (2, 'Grace Hopper');  -- 2 rows
        -- 3 books, split 2-and-1, exactly as in Examples 62-63
        INSERT INTO book(id, title, author_id) VALUES  -- a 3-row multi-VALUES insert
            (1, 'Notes on the Analytical Engine', 1),  -- Ada's first book
            (2, 'Sketch of the Analytical Engine', 1),  -- Ada's second book
            (3, 'The First Computer Bug', 2);  -- Grace's only book
        """
    )  # => same fixture as Examples 62-63 -- 2 authors, 3 books, split 2-and-1
    conn.commit()  # => persists the fixture before the two batched queries run


def main() -> (
    None
):  # => entry point -- setup(), a parent fetch, a batched IN(...) fetch, print
    conn: sqlite3.Connection = sqlite3.connect(
        ":memory:"
    )  # => a throwaway, process-local DB
    setup(conn)  # => builds the identical fixture Examples 62-63 used

    query_count: int = 0  # => tracks round trips -- watch this settle at 2, not 1 or 3
    authors: list[tuple[int, str]] = conn.execute(  # => query #1 -- the parent fetch
        "SELECT id, name FROM author"  # => no WHERE -- every author row, unconditionally
    ).fetchall()  # => drains the cursor -- 2 author rows, exactly like Example 62's first query
    query_count += (
        1  # => query #1 -- the parent rows, exactly like Example 62's first query
    )

    author_ids: list[int] = [
        author_id for author_id, _ in authors
    ]  # => just the ids, in order
    # => extracts JUST the ids from the (id, name) pairs -- discards name via the _ placeholder
    # Builds "?, ?, ..." -- ONE placeholder per id -- the values themselves stay fully parameterized.
    placeholders: str = ",".join("?" for _ in author_ids)  # => "?,?" for 2 authors
    books: list[tuple[int, str]] = (
        conn.execute(  # => query #2 -- the ONLY child fetch, batched
            f"SELECT author_id, title FROM book WHERE author_id IN ({placeholders})",
            # => the f-string only splices in "?,?" placeholder MARKS -- never a real data value
            author_ids,  # => co-20 -- every id is still bound as a real parameter, never interpolated
        ).fetchall()
    )  # => query #2 -- ALL children for EVERY parent, in a single batched round trip
    query_count += (
        1  # => the second and FINAL query -- independent of how many authors there are
    )

    grouped: dict[int, list[str]] = {}  # => empty until the loop below fills it in
    for (
        author_id,
        title,
    ) in books:  # => groups the flat rows by author_id, in plain Python
        grouped.setdefault(author_id, []).append(
            title
        )  # => builds the grouping in Python
        # => same setdefault-and-append pattern Example 63 used, applied to a different key

    for author_id, author_name in authors:  # => iterates in the ORIGINAL author order
        print(
            author_name, grouped.get(author_id, [])
        )  # => .get(..., []) -- safe for zero books
        # => Output: identical two lines to Examples 62-63 -- same data, now via 2 total queries
    print(
        f"queries executed: {query_count}"
    )  # => 2 -- one parent query PLUS one batched fetch
    conn.close()  # => releases the in-memory connection


if __name__ == "__main__":  # => guards main() so importing this module never runs it
    main()  # => runs the whole demonstration end to end
