"""Example 75: pytest verification for Paradigm Mismatch Cost."""

from example import solve_imperative_painfully, solve_with_constraints


def test_both_versions_find_a_correct_triple_summing_to_fifteen() -> None:
    digits = [1, 4, 5, 6, 9, 10]  # => same search space as the module-level demo
    painful = solve_imperative_painfully(digits)
    clean = solve_with_constraints(digits)
    assert painful is not None and sum(painful) == 15  # => a genuinely valid triple
    assert clean is not None and sum(clean) == 15  # => a genuinely valid triple, possibly a different one
    assert len(set(painful)) == 3  # => all three digits distinct, per the constraint
    assert len(set(clean)) == 3


def test_a_search_space_with_no_valid_triple_returns_none_in_both_versions() -> None:
    digits = [1, 1, 1]  # => only one distinct digit repeated -- no combination of three distinct digits exists
    assert solve_imperative_painfully(digits) is None
    assert solve_with_constraints(digits) is None


# => Run: pytest -- Output: 2 passed
