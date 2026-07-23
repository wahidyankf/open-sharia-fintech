"""Example 3: pytest verification for Classify Pure vs. Impure Functions."""

from example import is_pure, mutate_double, pure_double


def test_only_pure_double_is_flagged_pure() -> None:
    assert is_pure("pure_double") is True  # => the only function with zero side effects
    assert is_pure("loud_double") is False  # => prints -- a side effect
    assert is_pure("mutate_double") is False  # => mutates its argument -- a side effect


def test_mutate_double_changes_caller_list() -> None:
    items = [1, 2]
    mutate_double(items)  # => appends items[-1] * 2 in place
    assert items == [1, 2, 4]  # => the CALLER's own list object was mutated
    assert pure_double(3) == 6  # => pure_double never touches items at all


# => Run: pytest -- Output: 2 passed
