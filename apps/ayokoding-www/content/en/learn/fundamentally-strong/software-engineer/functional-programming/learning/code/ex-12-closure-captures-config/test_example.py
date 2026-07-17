"""Example 12: pytest verification for A Closure Capturing a Threshold."""

from example import make_validator


def test_closures_vary_with_their_captured_threshold() -> None:
    passes_ten = make_validator(10)
    passes_hundred = make_validator(100)
    assert passes_ten(15) is True
    assert passes_hundred(15) is False


# => Run: pytest -- Output: 1 passed
