"""Example 78: pytest verification for Paradigm Portfolio README."""

from example import (
    MATRIX,
    EvensSquaredOO,
    evens_squared_declarative,
    evens_squared_functional,
    evens_squared_imperative,
)


def test_matrix_covers_all_four_solutions_with_a_criterion_each() -> None:
    assert len(MATRIX) == 4  # => one row per solution, none missing
    for row in MATRIX:  # => every row must actually carry a criterion value, not a placeholder
        assert isinstance(row.testable_in_isolation, bool)
        assert row.solution_ref != ""


def test_every_solution_in_the_matrix_actually_agrees() -> None:
    sample = [10, 11, 12, 13]  # => a second independent sample
    assert evens_squared_imperative(sample) == [100, 144]
    assert EvensSquaredOO().apply(sample) == [100, 144]
    assert list(evens_squared_functional(tuple(sample))) == [100, 144]
    assert evens_squared_declarative(sample) == [100, 144]


# => Run: pytest -- Output: 2 passed
