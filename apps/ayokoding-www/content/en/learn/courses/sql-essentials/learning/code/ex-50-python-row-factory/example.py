# pyright: strict
"""Example 50: Python Row Factory."""

import sqlite3  # => sqlite3 is stdlib -- no pip install needed

conn: sqlite3.Connection = sqlite3.connect(":memory:")  # => opens an in-memory database
# row_factory swaps the default plain-tuple row shape for sqlite3.Row -- every
# row returned from now on supports BOTH positional AND column-name access.
conn.row_factory = sqlite3.Row  # => applies to every cursor opened after this line

conn.execute(
    "CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
)  # => id + name
conn.execute(
    "INSERT INTO author (name) VALUES ('Ada Lovelace')"
)  # => id auto-assigns to 1
conn.commit()  # => persists the insert

cur: sqlite3.Cursor = conn.cursor()  # => a cursor executes SQL and holds results
cur.execute("SELECT id, name FROM author")  # => 1 row, not yet fetched
row: sqlite3.Row | None = cur.fetchone()  # => a sqlite3.Row, not a plain tuple
if row is not None:  # => narrows away None so indexing below is type-safe
    # row["name"] reads by COLUMN NAME -- no need to remember column ORDER,
    # unlike the plain-tuple row[1] this same query would otherwise return.
    print(row["id"], row["name"])  # => Output: 1 Ada Lovelace

conn.close()  # => releases the connection -- irrelevant here since it's in-memory
