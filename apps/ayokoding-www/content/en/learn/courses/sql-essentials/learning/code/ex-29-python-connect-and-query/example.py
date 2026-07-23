# pyright: strict
"""Example 29: Python Connect And Query."""

import sqlite3  # => sqlite3 is stdlib -- no pip install needed (co-19)


def fetch_authors(
    conn: sqlite3.Connection,
) -> list[tuple[int, str]]:  # => a reusable helper
    # => typed signature (DD-39): takes a Connection, returns a list of (int, str) tuples
    """Return every author row as (id, name) tuples, ordered by id."""
    cur: sqlite3.Cursor = conn.cursor()  # => a Cursor runs statements against conn
    cur.execute("SELECT id, name FROM author ORDER BY id")
    # => sends the SQL text to the engine -- nothing is fetched into Python yet
    rows: list[tuple[int, str]] = cur.fetchall()
    # => fetchall() (co-21) pulls every remaining row as a list of tuples at once
    return rows  # => hands the fully-materialized list back to the caller


def main() -> None:  # => the script's entry point
    conn: sqlite3.Connection = sqlite3.connect(":memory:")
    # => connect() (co-19) opens a Connection -- ":memory:" avoids touching disk here
    cur: sqlite3.Cursor = conn.cursor()  # => a cursor scoped to this connection
    cur.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    # => same DDL as the CLI examples -- Python drives the identical SQL engine
    cur.execute(  # => passes a single multi-value INSERT string
        "INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace'), (2, 'Grace Hopper')"
    )  # => inserts 2 rows in one round-trip
    conn.commit()  # => commit() (co-19) makes the write durable and visible

    rows: list[tuple[int, str]] = fetch_authors(conn)
    # => calls the typed helper above -- rows is [(1, 'Ada Lovelace'), (2, 'Grace Hopper')]
    for row in rows:  # => iterates the list of (id, name) tuples
        print(row)  # => Output: (1, 'Ada Lovelace') then (2, 'Grace Hopper')

    conn.close()  # => releases the connection's resources
    # => always close what you open -- especially before the process exits


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
