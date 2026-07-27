"""Example 20: B-Tree Leaf Split and Separator Promotion."""

import bisect  # => stdlib module for the sorted insert this example performs before splitting

# When a leaf's key count exceeds its capacity, it SPLITS into two leaves and
# promotes the median key upward as a separator (co-09) -- the tree stays
# balanced because every leaf keeps roughly half its former keys, never a
# lopsided remainder.
MAX_KEYS: int = (
    4  # => a small capacity so this example can trigger a split with few inserts
)


def insert_and_maybe_split(
    leaf: list[int], key: int
) -> tuple[
    list[int], list[int] | None, int | None
]:  # => (left, right-or-None, separator-or-None)
    bisect.insort(leaf, key)  # => insert first, keeping the leaf sorted
    if len(leaf) <= MAX_KEYS:  # => still under capacity: no split needed
        return (
            leaf,
            None,
            None,
        )  # => the caller's own leaf, unchanged in identity, no split occurred
    mid = len(leaf) // 2  # => the median position -- splits as evenly as possible
    left, separator, right = (
        leaf[:mid],
        leaf[mid],
        leaf[mid + 1 :],
    )  # => slice into three pieces
    return left, right, separator  # => two leaves plus the promoted key between them


leaf: list[int] = [10, 20, 30, 40]  # => already at MAX_KEYS capacity
left, right, separator = insert_and_maybe_split(
    leaf, 25
)  # => this insert forces a split
print((left, separator, right))  # => Output: ([10, 20], 25, [30, 40])

assert left == [10, 20]  # => the left leaf keeps the smaller half
assert right == [30, 40]  # => the right leaf keeps the larger half
assert (
    separator == 25
)  # => the median key is promoted, not simply dropped or duplicated
print("ex-20 OK")  # => Output: ex-20 OK
