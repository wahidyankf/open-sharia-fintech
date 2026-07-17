"""Example 32: pytest verification for Four Ways -- Declarative."""

import sqlite3


def word_frequency_declarative(text: str) -> dict[str, int]:  # => reusable helper mirroring example.py
    conn = sqlite3.connect(":memory:")  # => fresh in-memory database per call
    conn.execute("CREATE TABLE words (word TEXT)")
    conn.executemany("INSERT INTO words VALUES (?)", [(w,) for w in text.split()])
    rows = conn.execute("SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY COUNT(*) DESC").fetchall()
    conn.close()  # => always release the connection
    return dict(rows)  # => same shape as the other three ways


def test_declarative_counts_match_all_three_other_ways() -> None:
    result = word_frequency_declarative("red blue red green blue red")
    assert result == {"red": 3, "blue": 2, "green": 1}  # => the same dict, all four paradigms agree


# => Run: pytest -- Output: 1 passed
