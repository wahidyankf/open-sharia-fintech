# pyright: strict
"""Example 30: Python Parameterized Insert."""

import sqlite3  # => sqlite3 is stdlib -- no pip install needed (co-19)


def insert_author(conn: sqlite3.Connection, name: str) -> int:  # => a reusable helper
    # => typed signature (DD-39): takes a Connection and a str, returns the new row's id
    """Insert one author by name using a ?-placeholder and return its new id."""
    cur: sqlite3.Cursor = conn.cursor()  # => a cursor scoped to this connection
    cur.execute("INSERT INTO author(name) VALUES (?)", (name,))
    # => ? is a positional placeholder (co-20) -- name is bound as DATA, never as SQL text
    conn.commit()  # => makes the insert durable before we report success
    new_id: int = cur.lastrowid if cur.lastrowid is not None else -1
    # => lastrowid is the rowid the engine just assigned -- Optional[int], so we narrow it
    return new_id  # => hands the concrete int id back to the caller


def main() -> None:  # => the script's entry point
    conn: sqlite3.Connection = sqlite3.connect(":memory:")
    # => a fresh in-memory database for this script run
    conn.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    # => execute() on the Connection directly, without a separate cursor object

    # A value containing SQL syntax -- proves the placeholder binds it as DATA, not code.
    name: str = "Ada Lovelace; DROP TABLE author;--"
    # => if this string were interpolated into raw SQL text, it would drop the table
    new_id: int = insert_author(conn, name)
    # => calls the typed helper above -- the ? placeholder neutralizes the injection attempt
    print(f"inserted id={new_id}")  # => Output: inserted id=1

    cur: sqlite3.Cursor = conn.cursor()  # => a fresh cursor to verify the stored row
    cur.execute(
        "SELECT id, name FROM author"
    )  # => reads the table back to prove it survived
    rows: list[tuple[int, str]] = cur.fetchall()
    # => rows is [(1, 'Ada Lovelace; DROP TABLE author;--')] -- table still exists, untouched
    for row in rows:  # => iterates the single result row
        print(row)  # => Output: (1, 'Ada Lovelace; DROP TABLE author;--')

    conn.close()  # => releases the connection's resources


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
