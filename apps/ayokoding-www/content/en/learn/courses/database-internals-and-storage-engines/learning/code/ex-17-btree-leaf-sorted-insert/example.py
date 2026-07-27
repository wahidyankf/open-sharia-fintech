"""Example 17: B-Tree Leaf -- Sorted Insert."""

import bisect

# A B-tree (and B+-tree) leaf holds its keys in SORTED order at all times
# (co-07) -- bisect.insort finds the correct insertion point and shifts the
# rest of the list over, so the invariant holds after every single insert,
# not just once a whole batch finishes.


def leaf_insert(
    leaf: list[int], key: int
) -> None:  # => keeps `leaf` sorted after this call returns
    bisect.insort(
        leaf, key
    )  # => O(n) insert-and-shift; O(log n) just to FIND the position


leaf: list[int] = []  # => a single leaf node modeled as a plain sorted list of keys
for key in [40, 10, 30, 20]:  # => insert in a deliberately UNsorted order
    leaf_insert(leaf, key)
    print(leaf)  # => Output: one growing, always-sorted list per insert

assert leaf == [
    10,
    20,
    30,
    40,
]  # => the leaf stays sorted after every single insertion, not just at the end
assert leaf == sorted(
    leaf
)  # => equivalent way to say the same thing: leaf never needs a final re-sort
print("ex-17 OK")  # => Output: ex-17 OK
