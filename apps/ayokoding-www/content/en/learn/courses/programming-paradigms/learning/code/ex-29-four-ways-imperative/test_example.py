"""Example 29: pytest verification for Four Ways -- Imperative."""

from example import word_frequency_imperative


def test_counts_match_the_known_sample() -> None:
    assert word_frequency_imperative("red blue red green blue red") == {
        "red": 3,
        "blue": 2,
        "green": 1,
    }  # => shared expected result across examples 29-32


# => Run: pytest -- Output: 1 passed
