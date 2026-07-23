"""Example 28: pytest verification for Paradigm Is Noise (Tiny Script)."""

from example import total_from_csv


def test_total_sums_the_second_column() -> None:
    assert total_from_csv("apple,3\nbanana,5\ncherry,2") == 10  # => 3 + 5 + 2


def test_a_single_row_still_works() -> None:
    assert total_from_csv("only,7") == 7  # => trivial one-row edge case


# => Run: pytest -- Output: 2 passed
