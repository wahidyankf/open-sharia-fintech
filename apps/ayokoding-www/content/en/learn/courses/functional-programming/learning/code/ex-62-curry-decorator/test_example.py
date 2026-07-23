"""Example 62: pytest verification for A @curry Decorator Auto-Currying by Arity."""

from example import add3


def test_partial_calls_accumulate_arguments_until_full_arity() -> None:
    assert add3(1, 2, 3) == 6
    assert add3(1)(2)(3) == 6
    assert add3(1, 2)(3) == 6


# => Run: pytest -- Output: 1 passed
