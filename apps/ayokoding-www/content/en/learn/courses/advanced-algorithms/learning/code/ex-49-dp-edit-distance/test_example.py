"""Example 49: pytest verification for Levenshtein Edit Distance."""

from example import edit_distance


def test_classic_kitten_to_sitting_example() -> None:
    assert edit_distance("kitten", "sitting") == 3


def test_identical_strings_have_zero_distance() -> None:
    assert edit_distance("hello", "hello") == 0


def test_completely_different_single_characters() -> None:
    assert edit_distance("a", "b") == 1  # => one substitution


# => Run: pytest -- Output: 3 passed
