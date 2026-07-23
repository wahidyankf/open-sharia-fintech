"""Example 53: pytest verification for A __repr__ That Round-Trips Through eval()."""

from example import Point


def test_repr_round_trips_through_eval() -> None:
    p: Point = Point(3, 4)
    rebuilt: Point = eval(repr(p))  # => reconstructs a Point from its own repr() string
    assert rebuilt == p  # => the reconstructed object is equal to the original


# => Run: pytest -- Output: 1 passed
