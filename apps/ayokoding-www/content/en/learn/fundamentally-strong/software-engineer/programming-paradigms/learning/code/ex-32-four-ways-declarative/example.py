"""Example 32: Four Ways -- Declarative."""

import sqlite3  # => the standard library's built-in SQL engine -- no external dependency needed

sample = "red blue red green blue red"  # => identical sample to examples 29-31

conn = sqlite3.connect(":memory:")  # => way #4 of 4: state the desired result, let SQLite compute it
conn.execute("CREATE TABLE words (word TEXT)")  # => declare the shape of the data
conn.executemany("INSERT INTO words VALUES (?)", [(w,) for w in sample.split()])  # => load every word
rows = conn.execute(  # => the query IS the algorithm -- no accumulator variable anywhere in this file
    "SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY COUNT(*) DESC"
    # => GROUP BY + COUNT(*) declares "the frequency of each word" -- no loop mechanics anywhere
).fetchall()  # => the query planner decided HOW to group and count; this call only asks for the rows
result = dict(rows)  # => turn the declared result into the same dict shape as examples 29-31
conn.close()  # => release the connection
# => an in-memory connection's data disappears once closed -- nothing to clean up on disk

print(result)  # => must match examples 29-31's dict exactly, across all four paradigms
# => Output: {'red': 3, 'blue': 2, 'green': 1}
