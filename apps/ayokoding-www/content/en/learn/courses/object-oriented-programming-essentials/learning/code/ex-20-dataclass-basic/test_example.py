"""Example 20: pytest verification for A Basic Dataclass."""

from example import Point


def test_generated_init_builds_point() -> None:
    p: Point = Point(1, 2)  # => positional construction via the auto-generated __init__
    assert p.x == 1
    assert p.y == 2


# => Run: pytest -- Output: 1 passed
