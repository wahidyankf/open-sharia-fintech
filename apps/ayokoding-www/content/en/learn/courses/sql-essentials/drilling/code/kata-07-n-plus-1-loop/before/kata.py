# pyright: strict
"""Kata 7 (before): one SELECT per author inside a loop -- N+1 round trips."""

import sqlite3


def books_by_author(conn: sqlite3.Connection) -> dict[str, list[str]]:
    query_count: int = 0
    result: dict[str, list[str]] = {}
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM author")
    authors: list[tuple[int, str]] = cur.fetchall()
    query_count += 1
    for author_id, name in authors:
        # THE BUG: one fresh SELECT for EVERY author, instead of one query total.
        cur.execute("SELECT title FROM book WHERE author_id = ?", (author_id,))
        titles: list[str] = [row[0] for row in cur.fetchall()]
        query_count += 1
        result[name] = titles
    print(f"queries issued: {query_count}")
    return result


conn: sqlite3.Connection = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
conn.execute(
    "CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER)"
)
conn.executemany(
    "INSERT INTO author(name) VALUES (?)",
    [("Ada Lovelace",), ("Grace Hopper",), ("Alan Turing",)],
)
conn.executemany(
    "INSERT INTO book(title, author_id) VALUES (?, ?)",
    [
        ("Notes", 1),
        ("COBOL Manual", 2),
        ("Compiler Notes", 2),
        ("On Computable Numbers", 3),
    ],
)
conn.commit()

print(books_by_author(conn))
conn.close()
