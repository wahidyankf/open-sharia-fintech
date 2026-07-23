"""Example 12: pytest verification for Expression vs Statement."""

from example import classify_via_expression, classify_via_statement


def test_both_forms_agree_across_a_range_of_inputs() -> None:
    for n in range(-5, 6):  # => sweep every integer from -5 through 5 inclusive
        assert classify_via_statement(n) == classify_via_expression(n)  # => must always match


def test_boundary_value_zero_is_non_negative_in_both_forms() -> None:
    assert classify_via_statement(0) == "non-negative"  # => zero is explicitly non-negative
    assert classify_via_expression(0) == "non-negative"  # => the expression form agrees


# => Run: pytest -- Output: 2 passed
