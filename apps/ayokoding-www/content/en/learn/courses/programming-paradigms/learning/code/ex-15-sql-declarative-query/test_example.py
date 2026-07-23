"""Example 15: pytest verification for SQL Declarative Query."""

import sqlite3


def top_n_words(words: list[str], n: int) -> list[tuple[str, int]]:  # => reusable helper for the test
    conn = sqlite3.connect(":memory:")  # => fresh in-memory database per call
    conn.execute("CREATE TABLE words (word TEXT)")  # => same schema as the module-level demo
    conn.executemany("INSERT INTO words VALUES (?)", [(w,) for w in words])  # => load all rows
    rows = conn.execute(
        "SELECT word, COUNT(*) AS c FROM words GROUP BY word ORDER BY c DESC, word LIMIT ?",
        (n,),  # => parameterized LIMIT -- avoids string-formatting SQL directly
    ).fetchall()
    conn.close()  # => always release the connection before returning
    return rows  # => list of (word, count) tuples


def test_top_three_matches_the_functional_word_count() -> None:
    words: list[str] = str("the cat sat on the mat the cat ran").split()  # => identical sentence to ex-01/ex-11
    rows = top_n_words(words, 3)  # => query the declarative top-3
    assert rows == [("the", 3), ("cat", 2), ("mat", 1)]  # => ties broken alphabetically


def test_rows_match_a_hand_counted_dict_for_every_word() -> None:
    words: list[str] = str("a b a c b a").split()  # => a: 3, b: 2, c: 1
    rows = top_n_words(words, 3)  # => request all three distinct words
    assert dict(rows) == {"a": 3, "b": 2, "c": 1}  # => every count must match a hand count


# => Run: pytest -- Output: 2 passed
