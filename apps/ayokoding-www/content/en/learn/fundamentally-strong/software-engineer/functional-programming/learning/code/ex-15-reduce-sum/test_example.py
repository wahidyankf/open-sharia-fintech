"""Example 15: pytest verification for reduce() Sums a List."""

from functools import reduce

from example import add


def test_reduce_sums_the_sequence() -> None:
    nums = [1, 2, 3, 4, 5]
    assert reduce(add, nums, 0) == 15 == sum(nums)


# => Run: pytest -- Output: 1 passed
