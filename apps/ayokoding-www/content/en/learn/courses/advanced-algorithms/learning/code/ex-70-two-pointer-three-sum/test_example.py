"""Example 70: pytest verification for 3-Sum via Two Pointers."""

from example import three_sum


def test_matches_the_classic_known_answer() -> None:
    result = sorted(three_sum([-1, 0, 1, 2, -1, -4]))
    assert result == [[-1, -1, 2], [-1, 0, 1]]


def test_no_valid_triplet_returns_an_empty_list() -> None:
    assert three_sum([1, 2, 3]) == []  # => all positive -- can never sum to zero


def test_every_returned_triplet_is_unique() -> None:
    result = three_sum([0, 0, 0, 0])  # => heavy duplication in the input
    assert result == [[0, 0, 0]]  # => only ONE triplet, despite four zeros available


# => Run: pytest -- Output: 3 passed
