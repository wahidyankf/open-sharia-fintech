"""Example 2: pytest verification for Referential Transparency by Substitution."""

from example import price_with_call, price_with_value


def test_call_and_value_agree() -> None:
    # => substituting add(2, 3) with its value 5 changes nothing about the result
    assert price_with_call() == price_with_value() == 50


# => Run: pytest -- Output: 1 passed
