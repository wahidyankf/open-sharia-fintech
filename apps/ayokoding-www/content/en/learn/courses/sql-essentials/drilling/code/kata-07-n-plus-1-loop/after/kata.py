# pyright: strict
"""Kata 7 (after): one LEFT JOIN replaces the per-author loop -- a single round trip."""

import sqlite3


def books_by_author(conn: sqlite3.Connection) -> dict[str, list[str]]:
    query_count: int = 0
    result: dict[str, list[str]] = {}
    cur = conn.cursor()
    # THE FIX: one LEFT JOIN fetches every author-book pair (or lone author) at once.
    cur.execute(
        "SELECT author.name, book.title FROM author "
        "LEFT JOIN book ON book.author_id = author.id "
        "ORDER BY author.name"
    )
    rows: list[tuple[str, str | None]] = cur.fetchall()
    query_count += 1
    for name, title in rows:
        result.setdefault(name, [])
        if title is not None:
            result[name].append(title)
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
