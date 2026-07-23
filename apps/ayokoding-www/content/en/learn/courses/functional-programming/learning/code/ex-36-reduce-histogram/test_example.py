"""Example 36: pytest verification for Building a Histogram with reduce."""

from functools import reduce

from example import add_to_histogram


def test_reduce_builds_a_correct_histogram() -> None:
    words = ["x", "y", "x"]
    histogram = reduce(add_to_histogram, words, {})
    assert histogram == {"x": 2, "y": 1}


# => Run: pytest -- Output: 1 passed
