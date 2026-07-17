"""Example 37: pytest verification for Chaining map, filter, and reduce."""

from functools import reduce


def test_pipeline_matches_the_equivalent_comprehension() -> None:
    orders = [12, 7, 25, 3, 18, 9]
    doubled = map(lambda amount: amount * 2, orders)
    significant = filter(lambda amount: amount > 20, doubled)
    total = reduce(lambda acc, amount: acc + amount, significant, 0)
    assert total == sum(a * 2 for a in orders if a * 2 > 20) == 110


# => Run: pytest -- Output: 1 passed
