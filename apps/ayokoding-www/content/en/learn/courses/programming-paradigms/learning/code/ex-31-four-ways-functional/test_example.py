"""Example 31: pytest verification for Four Ways -- Functional."""

from collections import Counter


def word_frequency_functional(text: str) -> dict[str, int]:  # => reusable helper mirroring example.py
    return dict(Counter(text.split()))  # => value-producing, no mutation of the caller's input


def test_functional_counts_match_the_other_three_ways() -> None:
    assert word_frequency_functional("red blue red green blue red") == {
        "red": 3,
        "blue": 2,
        "green": 1,
    }  # => identical to examples 29-30's result


# => Run: pytest -- Output: 1 passed
