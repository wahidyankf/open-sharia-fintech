"""Example 43: pytest verification for functools.wraps Preserves __name__."""

from example import careful_decorator, naive_decorator


def test_wraps_preserves_name_and_plain_decorator_does_not() -> None:
    @naive_decorator
    def naive() -> str:
        return "x"

    @careful_decorator
    def careful() -> str:
        return "x"

    assert naive.__name__ == "wrapper"  # => identity lost without functools.wraps
    assert careful.__name__ == "careful"  # => identity preserved with functools.wraps


# => Run: pytest -- Output: 1 passed
