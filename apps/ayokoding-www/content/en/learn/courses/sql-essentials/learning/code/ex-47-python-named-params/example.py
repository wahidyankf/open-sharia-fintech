# pyright: strict
"""Example 47: Python Named Params."""

import sqlite3  # => sqlite3 is stdlib -- no pip install needed

# ":memory:" is an ephemeral, file-less database -- perfect for a self-contained
# example that needs no cleanup and leaves nothing on disk.
conn: sqlite3.Connection = sqlite3.connect(":memory:")  # => opens an in-memory database
conn.execute(  # => a minimal one-table schema
    "CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"  # => id + name only
)  # => defines a minimal one-table schema
conn.execute("INSERT INTO author (id, name) VALUES (1, 'Ada Lovelace')")  # => author 1
conn.execute("INSERT INTO author (id, name) VALUES (2, 'Grace Hopper')")  # => author 2
conn.commit()  # => persists both inserts to this connection's database

cur: sqlite3.Cursor = conn.cursor()  # => a cursor executes SQL and holds results

# :name is a NAMED placeholder -- bound from a dict KEY, not positional order.
# This is the exact same injection-safety guarantee as `?` (Example 30), just
# addressed by name instead of position -- useful when a query has many params.
params: dict[str, str] = {"name": "Grace Hopper"}  # => the dict key MUST match :name
cur.execute(
    "SELECT id, name FROM author WHERE name = :name", params
)  # => :name bound from params
row: tuple[int, str] | None = cur.fetchone()  # => None if no row matched
print(row)  # => Output: (2, 'Grace Hopper')

conn.close()  # => releases the connection -- irrelevant here since it's in-memory
