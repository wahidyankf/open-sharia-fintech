"""Example 77: pytest verification for Stacking Multiple Decorators and Reasoning About Order."""

from example import call_order, double


def test_decorators_nest_outermost_first_innermost_last() -> None:
    call_order.clear()
    double(5)
    assert call_order == ["outer enter", "inner enter", "inner exit", "outer exit"]


# => Run: pytest -- Output: 1 passed
