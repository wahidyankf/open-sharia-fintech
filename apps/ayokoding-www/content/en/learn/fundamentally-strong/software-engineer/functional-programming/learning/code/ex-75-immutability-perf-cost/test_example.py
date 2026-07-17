"""Example 75: pytest verification for Measuring Persistent-Update Cost vs. In-Place Mutation."""

from example import ImmutablePoint, MutablePoint, bump_immutable, bump_mutable


def test_both_versions_reach_the_correct_final_value() -> None:
    n = 100
    assert bump_immutable(ImmutablePoint(0, 0), n).x == n
    assert bump_mutable(MutablePoint(0, 0), n).x == n


# => Run: pytest -- Output: 1 passed
