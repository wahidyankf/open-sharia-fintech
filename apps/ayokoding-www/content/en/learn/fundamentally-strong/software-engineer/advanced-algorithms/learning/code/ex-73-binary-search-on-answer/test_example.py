"""Example 73: pytest verification for Binary Search on the Answer."""

from example import can_ship_within_days, min_ship_capacity


def test_classic_known_answer() -> None:
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert min_ship_capacity(weights, days=5) == 15


def test_boundary_is_exact_one_below_fails_the_predicate() -> None:
    weights = [3, 2, 2, 4, 1, 4]
    capacity = min_ship_capacity(weights, days=3)
    assert can_ship_within_days(weights, capacity, 3) is True
    assert can_ship_within_days(weights, capacity - 1, 3) is False


def test_one_day_requires_capacity_equal_to_total_weight() -> None:
    weights = [5, 5, 5]
    assert min_ship_capacity(weights, days=1) == 15


# => Run: pytest -- Output: 3 passed
