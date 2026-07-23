"""Example 21: pytest verification for Constraint Buys Property."""

from example import uses_a_frozenset, uses_a_tuple


def test_shared_tuple_is_never_mutated_by_either_call() -> None:
    shared = (1, 2, 3)  # => fresh tuple, isolated from the module-level demo
    uses_a_tuple(shared)  # => call #1, discard the result -- only checking for mutation
    uses_a_tuple(shared)  # => call #2, discard the result
    assert shared == (1, 2, 3)  # => the original tuple is byte-identical to before either call


def test_shared_frozenset_is_never_mutated_and_has_no_mutating_methods() -> None:
    shared = frozenset({1, 2, 3})  # => fresh frozenset
    uses_a_frozenset(shared)  # => call once, discard the result
    assert shared == frozenset({1, 2, 3})  # => unchanged
    assert not hasattr(shared, "add")  # => the constraint: no in-place mutation method exists at all


# => Run: pytest -- Output: 2 passed
