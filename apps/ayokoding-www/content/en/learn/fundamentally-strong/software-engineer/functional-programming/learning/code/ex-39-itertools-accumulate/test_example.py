"""Example 39: pytest verification for Running Totals via accumulate."""

from itertools import accumulate


def test_accumulate_produces_prefix_sums() -> None:
    deposits = [10, 20, 30]
    assert list(accumulate(deposits)) == [10, 30, 60]
    assert list(accumulate(deposits, max)) == [10, 20, 30]


# => Run: pytest -- Output: 1 passed
