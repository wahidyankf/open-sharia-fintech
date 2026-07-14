# pyright: strict
"""Example 54: injection-UNSAFE query, built via f-string interpolation."""

import sqlite3  # => sqlite3 is stdlib -- no pip install needed

# The classic attack payload: it tries to CLOSE the current string literal,
# then chain a second, attacker-controlled statement onto the query.
PAYLOAD: str = "'; DROP TABLE book;--"

conn: sqlite3.Connection = sqlite3.connect(":memory:")  # => opens an in-memory database
conn.execute(
    "CREATE TABLE book (id INTEGER PRIMARY KEY, title TEXT NOT NULL)"
)  # => id + title
conn.execute(
    "INSERT INTO book (title) VALUES ('Alpha')"
)  # => one seed row, id auto-assigns to 1
conn.commit()  # => persists the seed row

# UNSAFE: f-string interpolation splices PAYLOAD directly into the SQL text --
# the query's STRUCTURE now depends on attacker-controlled input, not just its
# data. Whatever the attacker types becomes part of the statement itself.
unsafe_query: str = f"SELECT * FROM book WHERE title = '{PAYLOAD}'"
print(unsafe_query)  # => the query text now literally contains a 2nd statement

try:  # => attempts to run the attacker-shaped query text
    conn.execute(unsafe_query)  # => may raise, depending on the payload shape
except sqlite3.ProgrammingError as exc:
    # This Python 3.13.12 sqlite3 build refuses to run more than one SQL
    # statement per execute() call -- it blocks THIS specific payload shape.
    # That is NOT proof f-string interpolation is safe: it only means this
    # particular stacked-statement attack collides with an UNRELATED guard.
    # A same-statement payload (e.g. `' OR '1'='1`) still bypasses the
    # intended WHERE filter entirely when the query is built by interpolation.
    print(f"blocked: {exc}")  # => real sqlite3 error text, captured verbatim

cur: sqlite3.Cursor = conn.cursor()  # => a cursor executes SQL and holds results
cur.execute("SELECT count(*) FROM book")  # => confirms whether the table survived
count: tuple[int] = cur.fetchone()  # => a 1-tuple: (row_count,)
print(count[0])  # => Output: 1 -- the table happened to survive THIS attempt

conn.close()  # => releases the connection -- irrelevant here since it's in-memory
