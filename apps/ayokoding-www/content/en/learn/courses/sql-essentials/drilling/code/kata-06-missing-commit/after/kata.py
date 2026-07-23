# pyright: strict
"""Kata 6 (after): an explicit commit() before close() makes the write durable."""

import os
import sqlite3

DB_PATH: str = "kata.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn1: sqlite3.Connection = sqlite3.connect(DB_PATH)
conn1.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
conn1.commit()

conn1.execute("INSERT INTO author(name) VALUES ('Ada Lovelace')")
# THE FIX: commit() BEFORE close() -- the write is durable before the connection ends.
conn1.commit()
conn1.close()

conn2: sqlite3.Connection = sqlite3.connect(DB_PATH)
rows: list[tuple[int, str]] = conn2.execute("SELECT id, name FROM author").fetchall()
print(rows)
conn2.close()
os.remove(DB_PATH)
