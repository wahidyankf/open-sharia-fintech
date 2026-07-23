"""Example 71: pytest verification for An Applicative Validation That Accumulates All Errors."""

from example import (
    Invalid,
    combine3,
    validate_age,
    validate_password,
    validate_username,
)


def test_every_failing_rule_is_collected_not_just_the_first() -> None:
    result = combine3(validate_username("a"), validate_password("x"), validate_age(5))
    assert result == Invalid(
        ("username too short", "password too short", "must be at least 13")
    )


# => Run: pytest -- Output: 1 passed
