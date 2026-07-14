"""Example 48: pytest verification for A staticmethod Namespaced Utility."""

from example import Date


def test_staticmethod_callable_without_an_instance() -> None:
    assert (
        Date.is_leap(2024) is True
    )  # => called on the class itself, no Date(...) constructed
    assert Date.is_leap(1900) is False  # => the century-not-divisible-by-400 exception


# => Run: pytest -- Output: 1 passed
