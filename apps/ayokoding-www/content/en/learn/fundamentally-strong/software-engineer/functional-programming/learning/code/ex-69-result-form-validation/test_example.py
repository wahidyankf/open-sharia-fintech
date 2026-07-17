"""Example 69: pytest verification for Validating a Form, Short-Circuiting on the First Failing Rule."""

from example import Err, Ok, validate_signup


def test_the_failing_rule_is_the_one_reported() -> None:
    assert validate_signup("ana", "longenough", 20) == Ok("welcome, ana")
    assert validate_signup("an", "longenough", 20) == Err("username too short")
    assert validate_signup("ana", "short", 20) == Err("password too short")
    assert validate_signup("ana", "longenough", 10) == Err("must be at least 13")


# => Run: pytest -- Output: 1 passed
