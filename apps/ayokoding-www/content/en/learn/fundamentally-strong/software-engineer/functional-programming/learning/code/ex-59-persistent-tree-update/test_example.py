"""Example 59: pytest verification for A Persistent Binary Tree With a Structural-Sharing Update."""

from example import insert, to_sorted_list


def test_insert_shares_the_untouched_subtree() -> None:
    root_a = insert(insert(None, 10), 20)
    root_b = insert(root_a, 5)
    assert to_sorted_list(root_a) == [10, 20]
    assert to_sorted_list(root_b) == [5, 10, 20]
    assert (
        root_b.right is root_a.right
    )  # => the untouched right subtree is reused, not rebuilt


# => Run: pytest -- Output: 1 passed
