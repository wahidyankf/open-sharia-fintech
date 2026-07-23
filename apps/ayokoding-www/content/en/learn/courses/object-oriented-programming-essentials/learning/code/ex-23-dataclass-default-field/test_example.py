"""Example 23: pytest verification for A Dataclass Field with a Default Value."""

from example import Point


def test_omitted_field_uses_default_value() -> None:
    p: Point = Point(1, 2)  # => label not passed
    assert p.label == ""  # => the default from the field declaration applied


def test_explicit_field_overrides_default() -> None:
    p: Point = Point(1, 2, label="origin")
    assert p.label == "origin"


# => Run: pytest -- Output: 2 passed
