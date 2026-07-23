"""Example 1: pytest verification for Pure vs. Impure -- Same Result Every Time."""

from example import add_impure, add_pure  # => imports both functions under test


def test_pure_add_is_repeatable() -> None:
    first = add_pure(2, 3)  # => first call
    second = add_pure(2, 3)  # => identical args, called again
    assert first == second == 5  # => pure function: always the same result


def test_impure_add_is_not_repeatable() -> None:
    first = add_impure(10, 10)  # => mutates the module-level counter as a side effect
    second = add_impure(10, 10)  # => SAME args, but counter_total has already grown
    assert first != second  # => impure function: repeat calls disagree


# => Run: pytest -- Output: 2 passed
