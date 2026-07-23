"""Example 28: pytest verification for Quickselect."""

import random

from example import quickselect


def test_every_rank_matches_sorted_index() -> None:
    random.seed(6)
    data: list[int] = random.sample(range(500), 25)
    expected = sorted(data)
    for k in range(len(data)):  # => checks EVERY rank, not just a couple samples
        assert quickselect(data, k) == expected[k]


def test_does_not_mutate_the_caller_list() -> None:
    data: list[int] = [5, 2, 8, 1]
    original = list(data)
    quickselect(data, k=1)
    assert data == original  # => the caller's list is untouched


# => Run: pytest -- Output: 2 passed
