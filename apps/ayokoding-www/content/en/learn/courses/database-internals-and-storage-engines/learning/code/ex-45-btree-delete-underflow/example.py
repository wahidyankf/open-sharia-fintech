"""Example 45: B-Tree Leaf Underflow -- Merge or Borrow."""
# Borrowing is tried first (co-09) -- merging is only the fallback when no sibling can spare a key.

CAPACITY = 4  # => the fixed leaf capacity used throughout this course's B-tree examples
MIN_KEYS = (
    CAPACITY // 2
)  # => a leaf below this many keys has UNDERFLOWED and must be repaired


def delete(
    leaves: list[list[int]], key: int
) -> None:  # => removes key, then repairs any underflow
    leaf_index = next(
        i for i, leaf in enumerate(leaves) if key in leaf
    )  # => which leaf holds the key
    leaves[leaf_index].remove(key)  # => the actual removal
    leaf = leaves[leaf_index]  # => the (possibly now underflowed) leaf that lost a key
    if (
        len(leaf) >= MIN_KEYS or len(leaves) == 1
    ):  # => still valid, or it is the only leaf left -- done
        return  # => no repair needed -- occupancy is still within bounds
    if (
        leaf_index + 1 < len(leaves) and len(leaves[leaf_index + 1]) > MIN_KEYS
    ):  # => right sibling can spare one
        borrowed = leaves[leaf_index + 1].pop(0)  # => take its smallest key
        leaf.append(borrowed)  # => and give it to the underflowed leaf
        return  # => borrowing alone repaired the underflow -- no merge needed
    if (
        leaf_index > 0 and len(leaves[leaf_index - 1]) > MIN_KEYS
    ):  # => else try the left sibling instead
        borrowed = leaves[leaf_index - 1].pop()  # => take its largest key
        leaf.insert(
            0, borrowed
        )  # => and give it to the underflowed leaf, keeping sort order
        return  # => borrowing from the left sibling also repaired the underflow
    if leaf_index + 1 < len(
        leaves
    ):  # => no sibling could spare a key -- MERGE with the right sibling
        leaf.extend(
            leaves.pop(leaf_index + 1)
        )  # => absorb the whole right sibling's keys
    else:  # => no right sibling exists -- merge with the left one instead
        leaves[leaf_index - 1].extend(
            leaves.pop(leaf_index)
        )  # => absorb THIS leaf into the left one


def is_valid(
    leaves: list[list[int]],
) -> bool:  # => every leaf is sorted, and non-solo leaves meet MIN_KEYS
    for leaf in leaves:  # => check each leaf independently
        if leaf != sorted(leaf):  # => a leaf's keys must always stay in ascending order
            return False  # => a leaf out of sort order is never a valid B-tree state
        if (
            len(leaf) < MIN_KEYS and len(leaves) > 1
        ):  # => underflowed, UNLESS it is the sole remaining leaf
            return False  # => an underflowed leaf with siblings means the repair logic has a bug
    return True  # => every leaf passed both the sort-order and occupancy checks


leaves = [[1, 2, 3, 4], [5, 6, 7, 8]]  # => two full leaves, each right at capacity
assert is_valid(leaves)  # => sanity check before the deletions begin

delete(
    leaves, 1
)  # => leaf 0 drops to [2,3,4] -- still >= MIN_KEYS(2), no repair needed
delete(leaves, 2)  # => leaf 0 drops to [3,4] -- exactly MIN_KEYS, still valid
delete(
    leaves, 3
)  # => leaf 0 drops to [4] -- now UNDER MIN_KEYS(2): underflow triggers repair
print(leaves)  # => Output: [[4, 5], [6, 7, 8]]

assert is_valid(leaves)  # => the repair (a borrow, in this case) restored a valid tree
print("ex-45 OK")  # => Output: ex-45 OK
