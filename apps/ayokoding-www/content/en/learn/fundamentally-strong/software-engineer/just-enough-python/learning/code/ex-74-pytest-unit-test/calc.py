"""Example 74: a pure typed function under pytest."""


def add(a: int, b: int) -> int:  # => no side effects -- trivial to test in isolation
    return a + b  # => returns the sum, nothing else
