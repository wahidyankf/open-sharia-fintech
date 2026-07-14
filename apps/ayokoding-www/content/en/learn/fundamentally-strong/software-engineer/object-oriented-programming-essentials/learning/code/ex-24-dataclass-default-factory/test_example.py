"""Example 24: pytest verification for default_factory for a Mutable Default."""

from example import Point


def test_each_instance_gets_its_own_list() -> None:
    a: Point = Point(1, 2)
    b: Point = Point(3, 4)
    a.tags.append("origin")  # => mutates a's list only
    assert a.tags == ["origin"]
    assert b.tags == []  # => b's list is independent, not shared with a


# => Run: pytest -- Output: 1 passed
