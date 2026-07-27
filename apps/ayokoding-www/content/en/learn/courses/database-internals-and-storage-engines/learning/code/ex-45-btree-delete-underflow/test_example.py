"""Example 45: pytest verification for B-Tree Leaf Underflow Repair."""

from example import delete, is_valid


def test_underflow_is_repaired_by_borrowing() -> None:
    leaves = [[1, 2, 3, 4], [5, 6, 7, 8]]
    delete(leaves, 1)
    delete(leaves, 2)
    delete(leaves, 3)
    assert is_valid(leaves)


def test_underflow_falls_back_to_merge_when_no_sibling_can_spare_a_key() -> None:
    leaves = [[1, 2], [3, 4]]
    delete(
        leaves, 1
    )  # => leaf 0 drops to [2] -- neither sibling has a spare key to lend
    assert is_valid(leaves)
    assert len(leaves) == 1  # => the underflowed leaf was merged away entirely


# => Run: pytest -- Output: 2 passed
