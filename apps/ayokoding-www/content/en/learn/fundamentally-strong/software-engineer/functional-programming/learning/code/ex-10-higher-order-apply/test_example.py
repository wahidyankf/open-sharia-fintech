"""Example 10: pytest verification for A Higher-Order apply Function."""

from example import apply, increment, triple


def test_apply_forwards_to_whichever_function_is_passed() -> None:
    assert apply(increment, 10) == 11
    assert apply(triple, 10) == 30
    assert apply(increment, 10) == increment(
        10
    )  # => apply changes nothing about the call


# => Run: pytest -- Output: 1 passed
