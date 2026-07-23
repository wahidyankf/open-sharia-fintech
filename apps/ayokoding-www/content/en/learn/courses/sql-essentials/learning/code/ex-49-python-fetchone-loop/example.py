# pyright: strict
"""Example 49: Python Fetchone Loop."""

import sqlite3  # => sqlite3 is stdlib -- no pip install needed

conn: sqlite3.Connection = sqlite3.connect(":memory:")  # => opens an in-memory database
conn.execute(
    "CREATE TABLE book (id INTEGER PRIMARY KEY, title TEXT NOT NULL)"
)  # => id + title
conn.execute(
    "INSERT INTO book (title) VALUES ('Notes on the Analytical Engine')"
)  # => book 1
conn.execute("INSERT INTO book (title) VALUES ('On Computable Numbers')")  # => book 2
conn.commit()  # => persists both inserts

cur: sqlite3.Cursor = conn.cursor()  # => a cursor executes SQL and holds results
cur.execute("SELECT id, title FROM book ORDER BY id")  # => 2 rows, not yet fetched

# fetchall() would load every row into memory at once; fetchone() streams ONE
# row per call instead -- the := walrus operator both assigns row AND checks
# it against None in the same expression, ending the loop at the sentinel.
row: tuple[int, str] | None  # => declared before the loop -- streamed one row at a time
while (row := cur.fetchone()) is not None:  # => None marks "no more rows"
    book_id, title = row  # => unpacks the 2-tuple into two typed names
    print(book_id, title)  # => one line printed per row, streamed

conn.close()  # => releases the connection -- irrelevant here since it's in-memory
