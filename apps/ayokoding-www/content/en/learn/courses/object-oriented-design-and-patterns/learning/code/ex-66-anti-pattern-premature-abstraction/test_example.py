"""Example 66: pytest verification that removing a premature abstraction simplifies the code."""

from example import (
    FlatRateTaxStrategy,
    count_lines_of_indirection,
    total_with_tax_premature,
    total_with_tax_simple,
)


def test_both_versions_produce_the_identical_result() -> None:
    premature = total_with_tax_premature(100.0, FlatRateTaxStrategy())  # => needs a strategy instance
    simple = total_with_tax_simple(100.0)  # => needs nothing extra
    assert premature == simple == 108.0  # => removing the abstraction changed nothing observable


def test_the_simplified_version_has_strictly_less_indirection() -> None:
    assert count_lines_of_indirection(strategy_based=True) > count_lines_of_indirection(strategy_based=False)  # => the win


# => Run: pytest -q -- Output: 2 passed
