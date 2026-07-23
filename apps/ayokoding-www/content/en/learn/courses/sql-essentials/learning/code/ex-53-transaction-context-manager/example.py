# pyright: strict
"""Example 53: Transaction Context Manager."""

import os  # => stdlib -- used below to reset the file between runs
import sqlite3  # => sqlite3 is stdlib -- no pip install needed

DB_PATH: str = "app.db"  # => a real file -- automatic rollback needs a durable baseline
if os.path.exists(DB_PATH):  # => start from a clean file every run
    os.remove(DB_PATH)  # => wipes any leftover file from a previous run

conn: sqlite3.Connection = sqlite3.connect(DB_PATH)  # => opens/creates the file
conn.execute(
    "CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
)  # => id + name
conn.execute(
    "INSERT INTO author (name) VALUES ('Ada Lovelace')"
)  # => id auto-assigns to 1
conn.commit()  # => durable baseline -- exactly 1 row

# `with conn:` (unlike `with open(...)`) does NOT close the connection -- it
# commits on a clean exit, or ROLLS BACK automatically if the block raises.
try:  # => opens a block that may raise
    with conn:  # => opens an implicit transaction for this block
        conn.execute(  # => second insert, about to be rolled back
            "INSERT INTO author (name) VALUES ('Grace Hopper')"  # => the row about to be undone
        )  # => visible inside the block, but not yet committed
        raise ValueError("simulated mid-transaction failure")  # => triggers rollback
except ValueError:  # => catches the simulated failure, after auto-rollback already ran
    print("caught: simulated mid-transaction failure")  # => Output line 1

cur: sqlite3.Cursor = conn.cursor()  # => a cursor executes SQL and holds results
cur.execute(
    "SELECT count(*) FROM author"
)  # => re-checks the row count after auto-rollback
count: tuple[int] = cur.fetchone()  # => a 1-tuple: (row_count,)
print(count[0])  # => Output line 2: 1 -- the failed insert left no partial write

conn.close()  # => releases the connection -- `with conn:` above did NOT close it
os.remove(DB_PATH)  # => tidy up the file this script created
