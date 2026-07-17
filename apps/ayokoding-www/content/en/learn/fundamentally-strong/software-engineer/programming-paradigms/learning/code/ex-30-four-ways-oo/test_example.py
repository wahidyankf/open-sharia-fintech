"""Example 30: pytest verification for Four Ways -- OO."""

from example import WordFrequencyCounter


def test_oo_counts_match_the_imperative_version() -> None:
    result = WordFrequencyCounter().count("red blue red green blue red").result()
    assert result == {"red": 3, "blue": 2, "green": 1}  # => identical to example 29's result


# => Run: pytest -- Output: 1 passed
