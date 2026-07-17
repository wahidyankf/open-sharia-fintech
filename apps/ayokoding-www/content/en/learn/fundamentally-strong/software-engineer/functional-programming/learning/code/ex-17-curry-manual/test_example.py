"""Example 17: pytest verification for Hand-Curry a Two-Argument Function."""

from example import add, add_curried


def test_curried_call_matches_uncurried_call() -> None:
    assert add_curried(2)(3) == add(2, 3) == 5


def test_partially_applied_curry_is_reusable() -> None:
    add_two = add_curried(2)
    assert add_two(10) == 12
    assert add_two(20) == 22


# => Run: pytest -- Output: 2 passed
