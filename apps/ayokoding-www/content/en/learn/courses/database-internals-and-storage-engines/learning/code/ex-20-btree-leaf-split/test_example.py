"""Example 20: pytest verification for B-Tree Leaf Split."""

from example import insert_and_maybe_split


def test_split_produces_two_leaves_and_a_separator() -> None:
    leaf = [10, 20, 30, 40]
    left, right, separator = insert_and_maybe_split(leaf, 25)
    assert left is not None and right is not None and separator is not None


def test_no_split_when_under_capacity() -> None:
    leaf = [10, 20]
    left, right, separator = insert_and_maybe_split(leaf, 15)
    assert (
        right is None and separator is None
    )  # => still under MAX_KEYS -- nothing was split
    assert left == [10, 15, 20]


# => Run: pytest -- Output: 2 passed
