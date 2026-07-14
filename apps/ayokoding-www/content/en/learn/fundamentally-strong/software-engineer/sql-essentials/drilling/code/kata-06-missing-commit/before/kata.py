# pyright: strict
"""Kata 6 (before): insert-then-close with no commit() -- the write never reaches disk."""

import os
import sqlite3

DB_PATH: str = "kata.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn1: sqlite3.Connection = sqlite3.connect(DB_PATH)
conn1.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
conn1.commit()  # the schema itself IS committed, so the table persists

conn1.execute("INSERT INTO author(name) VALUES ('Ada Lovelace')")
# THE BUG: no conn1.commit() here -- close() below discards the open transaction.
conn1.close()

# a completely fresh connection to the SAME file -- proves what actually landed on disk.
conn2: sqlite3.Connection = sqlite3.connect(DB_PATH)
rows: list[tuple[int, str]] = conn2.execute("SELECT id, name FROM author").fetchall()
print(rows)
conn2.close()
os.remove(DB_PATH)
