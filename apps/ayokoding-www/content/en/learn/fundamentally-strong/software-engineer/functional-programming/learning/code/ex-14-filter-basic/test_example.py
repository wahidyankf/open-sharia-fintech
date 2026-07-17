"""Example 14: pytest verification for filter() Keeps Only Evens."""

from example import is_even


def test_filter_keeps_only_predicate_matches() -> None:
    nums = [1, 2, 3, 4, 5, 6]
    result = list(filter(is_even, nums))
    assert result == [2, 4, 6]


# => Run: pytest -- Output: 1 passed
