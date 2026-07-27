"""Example 17: pytest verification for B-Tree Leaf Sorted Insert."""

from example import leaf_insert


def test_insert_keeps_a_list_sorted() -> None:
    leaf: list[int] = []
    for key in [5, 1, 4, 2, 3]:
        leaf_insert(leaf, key)
    assert leaf == [1, 2, 3, 4, 5]


def test_leaf_is_sorted_after_every_single_insert() -> None:
    leaf: list[int] = []
    for key in [9, 3, 7]:
        leaf_insert(leaf, key)
        assert leaf == sorted(
            leaf
        )  # => the invariant holds at EVERY step, not just at the end


# => Run: pytest -- Output: 2 passed
