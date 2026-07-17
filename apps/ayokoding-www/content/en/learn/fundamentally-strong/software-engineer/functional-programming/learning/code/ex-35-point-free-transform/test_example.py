"""Example 35: pytest verification for Rewriting a Lambda Pipeline Point-Free."""

from functools import partial
from typing import Callable

from example import add, compose, multiply


def test_point_free_matches_the_named_argument_version() -> None:
    with_named_arg: Callable[[int], int] = lambda x: multiply(2, add(3, x))
    point_free = compose(partial(multiply, 2), partial(add, 3))
    assert point_free(5) == with_named_arg(5) == 16


# => Run: pytest -- Output: 1 passed
