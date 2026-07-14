# pyright: strict
"""Example 63: N+1 Fixed with a Single JOIN."""

import sqlite3  # => stdlib DB-API module (co-19)


def setup(conn: sqlite3.Connection) -> None:  # => builds the SAME fixture as Example 62
    # Identical schema and seed data to Example 62 -- same problem, different query shape.
    conn.executescript(
        """
        -- same fixture shape as Example 62 -- comparing the FIX, not the data
        CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);  -- 1 parent table
        CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL);
        -- author_id is a plain integer column here too -- the fix is the QUERY, not the schema
        -- 2 authors, exactly as in Example 62
        INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace'), (2, 'Grace Hopper');  -- 2 rows
        -- 3 books, split 2-and-1, exactly as in Example 62
        INSERT INTO book(id, title, author_id) VALUES  -- a 3-row multi-VALUES insert
            (1, 'Notes on the Analytical Engine', 1),  -- Ada's first book
            (2, 'Sketch of the Analytical Engine', 1),  -- Ada's second book
            (3, 'The First Computer Bug', 2);  -- Grace's only book
        """
    )  # => same fixture as Example 62 -- 2 authors, 3 books, split 2-and-1
    conn.commit()  # => persists the fixture before the single report query runs


def main() -> (
    None
):  # => the entry point -- setup(), one JOIN query, then a print summary
    conn: sqlite3.Connection = sqlite3.connect(
        ":memory:"
    )  # => a throwaway, process-local DB
    setup(conn)  # => builds the identical fixture Example 62 used

    query_count: int = (
        0  # => tracks round trips -- watch this stay at 1, unlike Example 62's 3
    )
    # ONE query -- author JOIN book (co-13) -- replaces the whole per-author loop from Example 62.
    # No Python for loop issues per-author SELECTs anymore -- the JOIN does that work in SQL.
    rows: list[tuple[str, str]] = (
        conn.execute(  # => a single multi-line SQL string, one call
            """
        -- ONE query does what Example 62 needed 3 separate round trips to do
        SELECT author.name, book.title
        FROM author
        JOIN book ON book.author_id = author.id
        ORDER BY author.name, book.title
        """
        ).fetchall()
    )  # => 3 rows total, one PER BOOK, author name repeated where an author has 2 books
    query_count += (
        1  # => the round trip count no longer scales with the number of authors
    )

    # Groups the flat rows back into "author -> list of titles" in PLAIN PYTHON, not another query.
    grouped: dict[str, list[str]] = {}  # => empty until the loop below fills it in
    for author_name, title in rows:  # => iterates the 3 FLAT rows returned by the join
        grouped.setdefault(author_name, []).append(
            title
        )  # => builds the grouping in Python
        # => setdefault(author_name, []) creates the list on first sight, appends every time after

    for (
        name,
        titles,
    ) in grouped.items():  # => iterates the GROUPED dict, not the raw rows
        print(
            name, titles
        )  # => Output: identical two lines to Example 62, from ONE query
    print(f"queries executed: {query_count}")  # => 1 -- versus Example 62's 3
    conn.close()  # => releases the in-memory connection -- nothing to clean up on disk


if __name__ == "__main__":  # => guards main() so importing this module never runs it
    main()  # => runs the whole demonstration end to end
