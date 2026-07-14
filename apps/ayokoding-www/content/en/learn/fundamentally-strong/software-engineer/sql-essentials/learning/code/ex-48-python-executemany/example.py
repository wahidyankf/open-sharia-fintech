# pyright: strict
"""Example 48: Python Executemany."""

import sqlite3  # => sqlite3 is stdlib -- no pip install needed

conn: sqlite3.Connection = sqlite3.connect(":memory:")  # => opens an in-memory database
conn.execute(  # => a single-column-of-interest table, ideal for a bulk-insert demo
    "CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"  # => id + name only
)  # => a single-column-of-interest table, ideal for a bulk-insert demo

# executemany() runs the SAME statement once PER tuple in this list -- one bulk
# call instead of a Python loop issuing N separate .execute() round-trips.
rows: list[tuple[str]] = [("Ada Lovelace",), ("Grace Hopper",), ("Alan Turing",)]
# => 3 single-element tuples -- one tuple per row to insert
conn.executemany(  # => one bulk call, not 3 separate .execute() calls
    "INSERT INTO author (name) VALUES (?)", rows
)  # => 3 rows inserted in one call -- id auto-assigns 1, 2, 3
conn.commit()  # => persists all 3 inserts together

cur: sqlite3.Cursor = conn.cursor()  # => a cursor executes SQL and holds results
cur.execute("SELECT count(*) FROM author")  # => confirms all 3 rows landed
count: tuple[int] = cur.fetchone()  # => a 1-tuple: (row_count,)
print(count[0])  # => Output: 3

conn.close()  # => releases the connection -- irrelevant here since it's in-memory
