"""Example 54: pytest verification for Declarative Validation Rules."""

from example import validate


def test_input_satisfying_every_rule_passes() -> None:
    assert validate({"email": "a@example.com", "age": 30}) is None  # => no declared rule was violated


def test_bad_input_is_flagged_with_the_specific_failing_rule() -> None:
    assert validate({"email": "not-an-email", "age": 30}) == "email_has_at_sign"  # => names the exact rule
    assert validate({"age": 30}) == "has_email"  # => a different missing-field failure names a different rule


# => Run: pytest -- Output: 2 passed
