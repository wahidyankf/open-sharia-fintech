"""Example 54: pytest verification for One fmap Working on list and Option."""

from typing import Callable

from example import Nothing, Some, fmap


def test_the_same_fmap_dispatches_on_container_shape() -> None:
    double: Callable[[int], int] = lambda n: n * 2
    assert fmap(double, [1, 2]) == [2, 4]
    assert fmap(double, Some(3)) == Some(6)
    assert fmap(double, Nothing()) == Nothing()


# => Run: pytest -- Output: 1 passed
