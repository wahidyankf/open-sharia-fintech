"""Example 55: pytest verification for A Duck-Typed Function Over Mixed Types."""

from example import Circle, Square, total_area


def test_mixed_unrelated_types_sum_correctly() -> None:
    shapes: list[object] = [Circle(1.0), Square(2.0), Circle(2.0)]
    assert (
        round(total_area(shapes), 5) == 19.70795
    )  # => 3.14159 + 4.0 + 12.56636 (rounded)


# => Run: pytest -- Output: 1 passed
