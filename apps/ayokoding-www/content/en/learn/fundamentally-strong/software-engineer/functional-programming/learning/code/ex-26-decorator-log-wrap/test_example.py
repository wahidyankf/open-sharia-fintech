"""Example 26: pytest verification for A Logging Decorator Wraps a Function."""

from example import add


def test_decorator_preserves_the_result() -> None:
    assert add(2, 3) == 5  # => the wrapped call still returns the correct value


# => Run: pytest -- Output: 1 passed
