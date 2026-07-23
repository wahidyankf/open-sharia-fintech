"""Example 55: pytest verification for Backtracking Permutations."""

import math

from example import all_permutations


def test_permutation_count_is_n_factorial() -> None:
    for n in range(5):
        items = list(range(n))
        assert len(all_permutations(items)) == math.factorial(n)


def test_all_permutations_are_distinct() -> None:
    perms = all_permutations([1, 2, 3, 4])
    unique = {tuple(p) for p in perms}
    assert len(unique) == len(perms)


def test_empty_input_yields_one_empty_permutation() -> None:
    assert all_permutations([]) == [[]]


# => Run: pytest -- Output: 3 passed
