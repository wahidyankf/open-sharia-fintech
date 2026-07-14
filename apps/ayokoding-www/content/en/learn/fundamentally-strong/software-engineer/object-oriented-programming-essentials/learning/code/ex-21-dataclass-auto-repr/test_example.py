"""Example 21: pytest verification for A Dataclass's Auto-Generated __repr__."""

from example import Point


def test_generated_repr_names_every_field() -> None:
    p: Point = Point(1, 2)
    assert (
        repr(p) == "Point(x=1, y=2)"
    )  # => exact string the @dataclass decorator generated


# => Run: pytest -- Output: 1 passed
