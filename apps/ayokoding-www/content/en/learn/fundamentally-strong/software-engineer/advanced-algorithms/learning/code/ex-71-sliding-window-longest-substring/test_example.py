"""Example 71: pytest verification for Longest Substring Without Repeats."""

import random
import string

from example import (
    brute_force_longest_unique_substring,
    longest_unique_substring_length,
)


def test_matches_brute_force_on_random_strings() -> None:
    random.seed(121)
    for _ in range(20):
        s = "".join(random.choices("abc", k=12))  # => a small alphabet forces repeats
        assert longest_unique_substring_length(
            s
        ) == brute_force_longest_unique_substring(s)


def test_all_unique_characters_returns_full_length() -> None:
    s = string.ascii_lowercase[:10]  # => 10 distinct characters, no repeats at all
    assert longest_unique_substring_length(s) == 10


def test_empty_string_has_length_zero() -> None:
    assert longest_unique_substring_length("") == 0


# => Run: pytest -- Output: 3 passed
