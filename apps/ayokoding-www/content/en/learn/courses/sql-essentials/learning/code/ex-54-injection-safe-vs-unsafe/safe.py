# pyright: strict
"""Example 54: injection-SAFE query, built via a `?` bound parameter."""

import sqlite3  # => sqlite3 is stdlib -- no pip install needed

# The identical payload from unsafe.py -- same attacker input, different result.
PAYLOAD: str = "'; DROP TABLE book;--"

conn: sqlite3.Connection = sqlite3.connect(":memory:")  # => opens an in-memory database
conn.execute(
    "CREATE TABLE book (id INTEGER PRIMARY KEY, title TEXT NOT NULL)"
)  # => id + title
conn.execute(
    "INSERT INTO book (title) VALUES ('Alpha')"
)  # => one seed row, id auto-assigns to 1
conn.commit()  # => persists the seed row

cur: sqlite3.Cursor = conn.cursor()  # => a cursor executes SQL and holds results
# SAFE: `?` passes PAYLOAD as a bound VALUE, never as SQL text -- the query's
# structure is fixed at prepare time, before SQLite ever inspects the value.
cur.execute(
    "SELECT * FROM book WHERE title = ?", (PAYLOAD,)
)  # => PAYLOAD bound, not spliced
rows: list[tuple[int, str]] = cur.fetchall()  # => every matching row, fetched at once
print(rows)  # => Output: [] -- no title literally equals the payload string

cur.execute("SELECT count(*) FROM book")  # => confirms the table is fully intact
count: tuple[int] = cur.fetchone()  # => a 1-tuple: (row_count,)
print(count[0])  # => Output: 1 -- book table is fully intact, unaffected

conn.close()  # => releases the connection -- irrelevant here since it's in-memory
