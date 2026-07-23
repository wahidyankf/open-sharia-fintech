"""Example 32: pytest verification for A Computed Property Derived from Two Fields."""

from example import Rectangle


def test_perimeter_updates_after_width_changes() -> None:
    r: Rectangle = Rectangle(3.0, 4.0)
    assert r.perimeter == 14.0
    r.width = 10.0  # => mutate the field the property is derived from
    assert (
        r.perimeter == 28.0
    )  # => the computed value tracks the mutation automatically


# => Run: pytest -- Output: 1 passed
