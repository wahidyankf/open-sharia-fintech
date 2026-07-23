"""Example 29: pytest verification for A Read-Only Property."""

from example import Rectangle


def test_area_reads_as_plain_attribute() -> None:
    r: Rectangle = Rectangle(3.0, 4.0)
    assert r.area == 12.0  # => r.area, not r.area() -- property syntax, computed value


# => Run: pytest -- Output: 1 passed
