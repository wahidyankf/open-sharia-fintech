"""Example 18: B-Tree Point Lookup."""

import bisect

# Searching a single sorted leaf for one key is the base case every deeper
# B-tree lookup eventually bottoms out in (co-08) -- bisect_left finds the
# key's position in O(log n) comparisons, and an exact-match check tells
# present from absent.
leaf: list[int] = [10, 20, 30, 40, 50]  # => a pre-sorted leaf node


def lookup(
    leaf: list[int], key: int
) -> int | None:  # => returns the key if present, else None
    i = bisect.bisect_left(
        leaf, key
    )  # => O(log n): the position key WOULD occupy if present
    if (
        i < len(leaf) and leaf[i] == key
    ):  # => confirm the position actually holds this exact key
        return leaf[i]
    return None  # => key would fall here, but it does not actually exist in the leaf


print(lookup(leaf, 30))  # => Output: 30
print(lookup(leaf, 25))  # => Output: None

assert lookup(leaf, 30) == 30  # => a present key is found and returned
assert (
    lookup(leaf, 25) is None
)  # => an absent key returns None, not an incorrect neighbor
print("ex-18 OK")  # => Output: ex-18 OK
