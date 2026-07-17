"""Example 31: Segment Tree -- O(log n) Range-Minimum Queries."""

# A segment tree (co-15) stores, at each internal node, the aggregate (here,
# the MIN) of an entire array range -- built once in O(n), then answering any
# range-min query in O(log n) by combining O(log n) precomputed sub-ranges.

INF = float(  # => opens the sentinel construction
    "inf"  # => Python's built-in way to spell positive infinity as a float
)  # => the segment tree's "empty range" sentinel, larger than any value


class SegmentTreeMin:  # => a segment tree specialized for range-minimum queries
    def __init__(self, data: list[int]) -> None:  # => O(n): builds the whole tree once
        self.n = len(data)  # => the number of leaf elements
        self.tree: list[float] = [INF] * (  # => opens the array-backed tree allocation
            4 * self.n  # => 4n is a standard safe upper bound on array-based tree size
        )  # => 4n is a standard safe upper bound on array-based tree size
        self._build(data, 1, 0, self.n - 1)  # => builds the tree rooted at index 1

    def _build(  # => recursively fills every node with its range's minimum, bottom-up
        self,
        data: list[int],
        node: int,
        lo: int,
        hi: int,  # => [lo, hi] is this call's range
    ) -> (
        None
    ):  # => node uses the implicit-heap array encoding: children 2*node, 2*node+1
        if lo == hi:  # => a leaf: exactly one array element
            self.tree[node] = data[lo]  # => stores that element's own value directly
            return  # => nothing more to combine at a leaf
        mid = (lo + hi) // 2  # => splits this range roughly in half
        self._build(data, 2 * node, lo, mid)  # => builds the left child (index 2*node)
        self._build(
            data, 2 * node + 1, mid + 1, hi
        )  # => builds the right child (2*node+1)
        self.tree[node] = min(  # => this node's value is the min of its two children
            self.tree[2 * node], self.tree[2 * node + 1]
        )  # => combines children into this node's own min

    def query(self, lo: int, hi: int) -> float:  # => O(log n): min over [lo, hi]
        # => the public entry point -- always starts recursion at node 1, full range
        return self._query(1, 0, self.n - 1, lo, hi)  # => starts the recursion at root

    def _query(  # => the classic three-way split: outside, inside, or partial overlap
        self,
        node: int,
        node_lo: int,
        node_hi: int,
        lo: int,
        hi: int,  # => node covers [node_lo, node_hi]
    ) -> float:  # => the query range [lo, hi] never changes across the recursion
        if hi < node_lo or node_hi < lo:  # => this node's range is entirely OUTSIDE
            return INF  # => contributes nothing to a min -- INF is the identity
        if lo <= node_lo and node_hi <= hi:  # => this node's range is entirely INSIDE
            return self.tree[node]  # => the precomputed min covers this whole range
        mid = (node_lo + node_hi) // 2  # => this node PARTIALLY overlaps -- must split
        return min(  # => combines whatever both children individually contribute
            self._query(
                2 * node, node_lo, mid, lo, hi
            ),  # => recurses into the left half
            self._query(
                2 * node + 1, mid + 1, node_hi, lo, hi
            ),  # => and the right half
        )  # => combines whatever both halves contribute


data: list[int] = [
    5,
    2,
    8,
    1,
    9,
    3,
    7,
    4,
]  # => 8 unsorted integers, min is 1 at index 3
tree = SegmentTreeMin(data)  # => O(n): builds the tree once

print(tree.query(0, 3))  # => Output: 1 -- min of [5, 2, 8, 1]
print(tree.query(4, 7))  # => Output: 3 -- min of [9, 3, 7, 4]
print(tree.query(0, 7))  # => Output: 1 -- min of the whole array

assert tree.query(0, 3) == min(data[0:4])  # => confirms against a brute-force slice min
assert tree.query(4, 7) == min(data[4:8])  # => confirms another range against a slice
# => a single-element range is the INSIDE case -- returns the leaf's own value directly
assert tree.query(2, 2) == data[2]  # => a single-element range returns that element
print("ex-31 OK")  # => Output: ex-31 OK
