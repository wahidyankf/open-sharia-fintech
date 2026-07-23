"""Example 52: pytest verification for A Validation Pipeline Threading Result."""

from example import Err, Ok, validate_form


def test_one_bad_field_short_circuits_the_rest() -> None:
    assert validate_form("Ana", 30) == Ok("Ana, age 30")
    assert validate_form("", 30) == Err("name cannot be empty")
    assert validate_form("Ana", -1) == Err("age cannot be negative")


# => Run: pytest -- Output: 1 passed
