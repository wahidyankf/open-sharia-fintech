"""Example 40: pytest verification for order=True Adds Field-Tuple Comparisons."""

from example import Point


def test_instances_sort_by_field_tuple() -> None:
    points: list[Point] = [Point(2, 1), Point(1, 5), Point(1, 2)]
    points.sort()  # => uses the generated __lt__
    assert points == [Point(1, 2), Point(1, 5), Point(2, 1)]  # => (x, y) tuple order


# => Run: pytest -- Output: 1 passed
