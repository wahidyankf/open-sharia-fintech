# pyright: strict
"""Kata 4 (before): a WHERE clause built via string interpolation -- injectable."""

import sqlite3


def find_author_by_name(conn: sqlite3.Connection, name: str) -> list[tuple[int, str]]:
    cur = conn.cursor()
    # THE BUG: f-string interpolation lets the caller's input become SQL syntax,
    # not just a value -- the query text itself changes shape based on input.
    query = f"SELECT id, name FROM author WHERE name = '{name}'"
    cur.execute(query)
    return cur.fetchall()


conn: sqlite3.Connection = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
conn.executemany(
    "INSERT INTO author(name) VALUES (?)",
    [("Ada Lovelace",), ("Grace Hopper",)],
)
conn.commit()

# a crafted search value: no author is actually named this, but the OR clause
# it injects makes the WHERE condition true for every row in the table.
malicious_input: str = "nobody' OR '1'='1"
print(find_author_by_name(conn, malicious_input))
conn.close()
