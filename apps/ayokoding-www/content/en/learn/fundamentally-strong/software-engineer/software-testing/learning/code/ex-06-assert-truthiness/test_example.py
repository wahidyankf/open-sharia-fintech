# learning/code/ex-06-assert-truthiness/test_example.py
"""Example 6: Assert Truthiness."""


# ex-06: a plain boolean-condition assert, then a DELIBERATE failure right after it (co-03)
def is_even(n: int) -> bool:  # => the unit under test
    return n % 2 == 0  # => returns a genuine bool, not a string or 0/1


def test_truthiness_of_a_boolean_condition() -> (
    None
):  # => passes -- shown for contrast below
    assert is_even(
        4
    )  # => truthy assert: no "== True" needed, a bare bool is enough (co-03)


def test_truthiness_reports_operands_on_failure() -> (
    None
):  # => THIS ONE deliberately fails
    assert is_even(7), "7 should be odd, so is_even(7) must be False"  # => optional message string  # fmt: skip
    # => pytest prints BOTH the failing expression (is_even(7)) and this custom message --
    # => the introspection shown here is what "assert truthiness reports operands" means
