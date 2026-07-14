# pyright: strict
"""Example 52: Transaction Rollback."""

import os  # => stdlib -- used below to reset the file between runs
import sqlite3  # => sqlite3 is stdlib -- no pip install needed

DB_PATH: str = "app.db"  # => a real file -- rollback needs a durable baseline first
if os.path.exists(DB_PATH):  # => start from a clean file every run
    os.remove(DB_PATH)  # => wipes any leftover file from a previous run

conn: sqlite3.Connection = sqlite3.connect(DB_PATH)  # => opens/creates the file
conn.execute(
    "CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
)  # => id + name
conn.execute(
    "INSERT INTO author (name) VALUES ('Ada Lovelace')"
)  # => id auto-assigns to 1
conn.commit()  # => this ONE row is the durable baseline -- 1 row

conn.execute("BEGIN")  # => opens a new transaction around the next insert
conn.execute(  # => second insert, about to be rolled back
    "INSERT INTO author (name) VALUES ('Grace Hopper')"  # => the row about to be undone
)  # => this insert is visible WITHIN this connection right now
conn.rollback()  # => discards everything since BEGIN -- Grace Hopper is undone

# a fresh cursor verifies the post-rollback state matches the pre-transaction baseline
cur: sqlite3.Cursor = conn.cursor()  # => a cursor executes SQL and holds results
cur.execute("SELECT count(*) FROM author")  # => re-checks the row count after rollback
count: tuple[int] = cur.fetchone()  # => a 1-tuple: (row_count,)
print(count[0])  # => Output: 1 -- back to the pre-transaction baseline, not 2

conn.close()  # => releases the connection
os.remove(DB_PATH)  # => tidy up the file this script created
