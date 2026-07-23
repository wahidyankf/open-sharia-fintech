"""Example 27: pytest verification for A Recursive Factorial (No TCO)."""

from example import factorial


def test_factorial_matches_the_known_value() -> None:
    assert factorial(10) == 3628800
    assert factorial(0) == 1  # => base case


# => Run: pytest -- Output: 1 passed
