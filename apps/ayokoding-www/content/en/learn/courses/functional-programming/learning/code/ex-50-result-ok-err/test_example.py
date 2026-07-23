"""Example 50: pytest verification for A Hand-Rolled Ok/Err Result Type."""

from example import Err, Ok, divide


def test_result_carries_success_or_failure_as_a_value() -> None:
    assert divide(10, 2) == Ok(5.0)
    assert divide(10, 0) == Err("division by zero")


# => Run: pytest -- Output: 1 passed
