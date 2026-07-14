# pyright: strict
"""Kata 4 (after): a parameterized query neutralizes the same injection attempt."""

import sqlite3


def find_author_by_name(conn: sqlite3.Connection, name: str) -> list[tuple[int, str]]:
    cur = conn.cursor()
    # THE FIX: ? is a placeholder, not a splice point -- the driver binds `name`
    # as a single opaque value, so it can never change the shape of the query.
    cur.execute("SELECT id, name FROM author WHERE name = ?", (name,))
    return cur.fetchall()


conn: sqlite3.Connection = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
conn.executemany(
    "INSERT INTO author(name) VALUES (?)",
    [("Ada Lovelace",), ("Grace Hopper",)],
)
conn.commit()

malicious_input: str = "nobody' OR '1'='1"
print(find_author_by_name(conn, malicious_input))
conn.close()
