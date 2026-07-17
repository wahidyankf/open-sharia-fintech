"""Example 15: SQL Declarative Query."""

import sqlite3


words: list[str] = str("the cat sat on the mat the cat ran").split()  # => str(...) widens away the literal so split() returns list[str]

conn = sqlite3.connect(":memory:")  # => an in-process database -- no file, no server (stdlib only)
conn.execute("CREATE TABLE words (word TEXT)")  # => declare the shape of the data, not how to store it
conn.executemany("INSERT INTO words VALUES (?)", [(w,) for w in words])  # => load every word as a row

# => the query below STATES the desired result -- "top 3 words by frequency" -- SQLite figures out HOW
rows = conn.execute(
    "SELECT word, COUNT(*) AS n FROM words GROUP BY word ORDER BY n DESC, word LIMIT 3"
    # => GROUP BY: partition rows by word. ORDER BY n DESC: highest count first. LIMIT 3: only the top 3
).fetchall()  # => materialize the declared result as concrete rows

print(rows)  # => "the" (3), "cat" (2), then the first single-count word alphabetically
# => Output: [('the', 3), ('cat', 2), ('mat', 1)]

functional_counts = {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1, "ran": 1}  # => from example 11
top_word, top_count = rows[0]  # => unpack the declarative query's #1 row
print(functional_counts[top_word] == top_count)  # => the declarative and functional counts must agree
# => Output: True
conn.close()  # => release the in-memory connection
