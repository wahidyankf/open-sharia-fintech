# pyright: strict
"""Example 51: Transaction Commit."""

import os  # => stdlib -- used below to reset the file between runs
import sqlite3  # => sqlite3 is stdlib -- no pip install needed

DB_PATH: str = "app.db"  # => a real file, unlike Examples 47-50's ":memory:"
if os.path.exists(DB_PATH):  # => start from a clean file every run
    os.remove(DB_PATH)

# A FILE-based database (not ":memory:") is required here -- only a real file
# on disk can be reopened by a SECOND, independent connection below.
conn: sqlite3.Connection = sqlite3.connect(DB_PATH)  # => opens/creates the file
conn.execute(
    "CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
)  # => id + name
conn.execute("BEGIN")  # => explicitly opens a transaction
conn.execute(
    "INSERT INTO author (name) VALUES ('Ada Lovelace')"
)  # => id auto-assigns to 1
conn.commit()  # => makes the insert PERMANENT -- durable across connections
conn.close()  # => close the FIRST connection entirely

# A brand-new, independent connection to the SAME file -- proves the write
# survived past the original connection's lifetime, not just in its own cache.
conn2: sqlite3.Connection = sqlite3.connect(
    DB_PATH
)  # => a SECOND, independent connection
cur: sqlite3.Cursor = conn2.cursor()  # => a cursor executes SQL and holds results
cur.execute("SELECT count(*) FROM author")  # => reads through the second connection
count: tuple[int] = cur.fetchone()  # => a 1-tuple: (row_count,)
print(count[0])  # => Output: 1 -- the committed write persisted

conn2.close()  # => releases the second connection
os.remove(DB_PATH)  # => tidy up the file this script created
