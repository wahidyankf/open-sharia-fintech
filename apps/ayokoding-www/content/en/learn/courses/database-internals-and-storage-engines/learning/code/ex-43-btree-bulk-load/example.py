"""Example 43: B-Tree Bulk Load vs Insert-One-by-One."""
# Bulk load and incremental insert (co-08) can differ in shape but must agree on every lookup.

import bisect  # => stdlib binary-search helper for sorted-list insertion

LEAF_CAPACITY = 4  # => each leaf page holds at most 4 keys before it must split


def bulk_load(
    sorted_keys: list[int], capacity: int
) -> list[list[int]]:  # => bottom-up, one linear pass
    return [  # => a list comprehension -- one leaf per capacity-sized slice
        sorted_keys[i : i + capacity]
        for i in range(0, len(sorted_keys), capacity)  # => a fixed-size slice
    ]  # => end of the bulk-load comprehension  # => chunk ALREADY-SORTED input directly -- no comparisons, no splits, just slicing


def insert_one(
    leaves: list[list[int]], key: int, capacity: int
) -> None:  # => classic incremental insert
    if not leaves:  # => the very first key ever inserted into an empty tree
        leaves.append([key])  # => the tree's first (and only) leaf so far
        return  # => nothing more to do for the very first key
    leaf_index = 0  # => find which leaf this key belongs in, by comparing to each leaf's first key
    for i, leaf in enumerate(leaves):  # => walk leaves left to right
        if key < leaf[0]:  # => key belongs BEFORE this leaf -- stop at the previous one
            break  # => leaf_index already points at the right leaf
        leaf_index = (
            i  # => keep tracking the rightmost leaf whose start is still <= key
        )
    leaf = leaves[leaf_index]  # => the leaf this key will be inserted into
    bisect.insort(leaf, key)  # => insert keeping the leaf internally sorted
    if (
        len(leaf) > capacity
    ):  # => the leaf overflowed -- split it in two, like a real B-tree
        mid = len(leaf) // 2  # => the split point -- roughly half the keys on each side
        leaves[leaf_index] = leaf[:mid]  # => left half stays at this position
        leaves.insert(
            leaf_index + 1, leaf[mid:]
        )  # => right half becomes a brand-new leaf


def lookup(
    leaves: list[list[int]], key: int
) -> bool:  # => point lookup across the leaf chain
    return any(
        key in leaf for leaf in leaves
    )  # => a real B-tree binary-searches per leaf; O(n) here for clarity


sorted_keys = list(range(0, 20, 2))  # => [0, 2, 4, ..., 18] -- ten pre-sorted keys
bulk_leaves = bulk_load(
    sorted_keys, LEAF_CAPACITY
)  # => one linear pass, chunked geometry
incremental_leaves: list[list[int]] = []  # => built up key-by-key instead
for key in sorted_keys:  # => insert the SAME keys, one at a time
    insert_one(
        incremental_leaves, key, LEAF_CAPACITY
    )  # => grow the tree incrementally, key by key

print(bulk_leaves)  # => Output: [[0, 2, 4, 6], [8, 10, 12, 14], [16, 18]]
print(incremental_leaves)  # => Output: [[0, 2], [4, 6], [8, 10], [12, 14, 16, 18]]

test_keys = sorted_keys + [
    1,
    3,
    99,
]  # => every real key, plus some keys that should be absent
bulk_answers = [
    lookup(bulk_leaves, k) for k in test_keys
]  # => query the bulk-loaded tree
incremental_answers = [
    lookup(incremental_leaves, k) for k in test_keys
]  # => query the incremental tree
assert (
    bulk_answers == incremental_answers
)  # => SAME lookup answers despite DIFFERENT leaf geometry
print("ex-43 OK")  # => Output: ex-43 OK
