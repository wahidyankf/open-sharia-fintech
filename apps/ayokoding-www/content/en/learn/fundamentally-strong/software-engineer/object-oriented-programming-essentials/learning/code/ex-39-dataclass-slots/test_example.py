"""Example 39: pytest verification for slots=True Drops Per-Instance __dict__."""

import pytest

from example import Point


def test_slots_instance_has_no_dict() -> None:
    p: Point = Point(1, 2)
    assert not hasattr(
        p, "__dict__"
    )  # => __slots__ replaces the usual per-instance __dict__


def test_undeclared_attribute_assignment_raises() -> None:
    p: Point = Point(1, 2)
    with pytest.raises(AttributeError):
        p.z = 3  # type: ignore  # => z is not a declared field -- slots rejects it outright


# => Run: pytest -- Output: 2 passed
