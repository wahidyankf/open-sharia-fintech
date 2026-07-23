"""Example 6: pytest verification for the Merge Invariant Check."""

from example import merge_with_invariant_check


def test_invariant_holds_across_uneven_length_halves() -> None:
    result = merge_with_invariant_check(
        [1, 2, 3], [4, 5]
    )  # => left runs out first, right has leftovers
    assert result == [1, 2, 3, 4, 5]  # => confirms leftover elements still land right


def test_invariant_holds_with_duplicate_keys() -> None:
    result = merge_with_invariant_check(
        [1, 3], [1, 3]
    )  # => duplicate keys exercise the stable "<=" tie-break
    assert result == [1, 1, 3, 3]  # => confirms duplicates merge into correct order


# => Run: pytest -- Output: 2 passed
