"""Example 54: pytest verification for Backtracking Subsets."""

from example import all_subsets


def test_subset_count_is_two_to_the_n() -> None:
    for n in range(6):
        items = list(range(n))
        assert len(all_subsets(items)) == 2**n


def test_no_duplicate_subsets_are_generated() -> None:
    subsets = all_subsets([1, 2, 3, 4])
    unique = {tuple(s) for s in subsets}
    assert len(unique) == len(subsets)


def test_empty_input_yields_only_the_empty_subset() -> None:
    assert all_subsets([]) == [[]]


# => Run: pytest -- Output: 3 passed
