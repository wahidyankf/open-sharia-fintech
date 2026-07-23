"""Example 23: pytest verification for Two-Pointer Pair Sum."""

from example import two_pointer_pair_sum


def test_finds_a_matching_pair() -> None:
    result = two_pointer_pair_sum([1, 2, 3, 4, 5], target=7)
    assert result is not None
    assert sum(result) == 7  # => e.g. (2, 5) or (3, 4) -- either is a valid answer


def test_returns_none_when_no_pair_matches() -> None:
    assert two_pointer_pair_sum([1, 2, 3], target=100) is None


def test_two_element_array_checks_the_single_available_pair() -> None:
    assert two_pointer_pair_sum([2, 5], target=7) == (2, 5)


# => Run: pytest -- Output: 3 passed
