"""Example 67: Segment Tree vs Fenwick Tree -- Same Prefix-Sum Answers, Different Cost."""

# Both structures answer prefix-sum + point-update in O(log n) (co-14,
# co-15) -- but a Fenwick tree needs only O(n) space and a handful of lines
# (Example 30), while a segment tree needs O(4n) space and more code, in
# exchange for handling queries a Fenwick tree CAN'T (like range-min).


class FenwickTree:  # => identical to Example 30's implementation
    def __init__(self, n: int) -> None:  # => allocates the flat backing array
        self.n = n  # => the number of elements tracked
        self.tree: list[int] = [0] * (n + 1)  # => O(n) space -- a single flat array

    def update(self, i: int, delta: int) -> None:  # => applies delta at index i
        i += 1  # => converts to Fenwick's 1-indexed internal scheme
        while i <= self.n:  # => climbs through every ancestor this index touches
            self.tree[i] += delta  # => applies the delta at this ancestor node
            i += i & (
                -i
            )  # => THE FENWICK TRICK: jumps to the next responsible ancestor

    def prefix_sum(self, i: int) -> int:  # => sum of elements [0..i], inclusive
        i += 1  # => converts to Fenwick's 1-indexed internal scheme
        total = 0  # => running prefix sum
        while i > 0:  # => walks DOWN through the ancestors that cover this prefix
            total += self.tree[i]  # => accumulates this ancestor's contribution
            i -= i & (-i)  # => THE FENWICK TRICK: jumps to the next covering ancestor
        return total  # => the completed prefix sum


class SegmentTreeSum:  # => a sum-tracking segment tree -- more code, more memory
    def __init__(self, n: int) -> None:  # => allocates the recursive tree array
        self.n = n  # => the number of elements tracked
        self.tree: list[int] = [0] * (
            4 * n
        )  # => O(4n) space -- 4x a Fenwick tree's array

    def update(
        self, i: int, delta: int
    ) -> None:  # => public entry point for a point update
        self._update(
            1, 0, self.n - 1, i, delta
        )  # => starts the recursive descent at the root

    def _update(
        self, node: int, lo: int, hi: int, i: int, delta: int
    ) -> None:  # => recursive descent
        if lo == hi:  # => reached the LEAF representing index i
            self.tree[node] += delta  # => applies the delta directly
            return  # => nothing more to do at a leaf
        mid = (lo + hi) // 2  # => splits this node's range in half
        if i <= mid:  # => index i lives in the LEFT half
            self._update(2 * node, lo, mid, i, delta)  # => recurse into the left child
        else:  # => index i lives in the RIGHT half
            self._update(
                2 * node + 1, mid + 1, hi, i, delta
            )  # => recurse into the right child
        self.tree[node] = (
            self.tree[2 * node] + self.tree[2 * node + 1]
        )  # => re-merge from children

    def prefix_sum(self, i: int) -> int:  # => needs its OWN range-query traversal
        return self._query(1, 0, self.n - 1, 0, i)  # => queries the range [0, i]

    def _query(
        self, node: int, node_lo: int, node_hi: int, lo: int, hi: int
    ) -> int:  # => range sum
        if (
            hi < node_lo or node_hi < lo
        ):  # => this node's range is ENTIRELY outside [lo, hi]
            return 0  # => contributes nothing
        if (
            lo <= node_lo and node_hi <= hi
        ):  # => this node's range is ENTIRELY inside [lo, hi]
            return self.tree[
                node
            ]  # => its precomputed sum answers this subrange exactly
        mid = (node_lo + node_hi) // 2  # => a PARTIAL overlap -- must split and recurse
        return self._query(
            2 * node, node_lo, mid, lo, hi
        ) + self._query(  # => left contribution
            2 * node + 1,
            mid + 1,
            node_hi,
            lo,
            hi,  # => plus the right contribution
        )  # => closes the two-subquery sum


n = 12  # => 12 elements, both starting at zero
fenwick = FenwickTree(n)  # => the Fenwick-tree instance under test
segment_tree = SegmentTreeSum(n)  # => the segment-tree instance under test
updates: list[tuple[int, int]] = [  # => opens the shared update sequence
    (0, 5),  # => index 0, +5
    (3, 2),  # => index 3, +2
    (7, -1),  # => index 7, -1
    (11, 8),  # => index 11, +8
    (5, 4),  # => index 5, +4
]  # => the SAME sequence of point updates, applied to BOTH structures
for idx, delta in updates:  # => applies every update to both structures identically
    fenwick.update(idx, delta)  # => O(log n): a handful of pointer-arithmetic hops
    segment_tree.update(idx, delta)  # => O(log n): a recursive tree descent

queries: list[int] = [0, 3, 7, 11]  # => a spread of prefix-sum queries to compare
fenwick_answers = [fenwick.prefix_sum(i) for i in queries]  # => Fenwick's own answers
segment_answers = [
    segment_tree.prefix_sum(i) for i in queries
]  # => segment tree's own answers
print(fenwick_answers)  # => Output: [5, 7, 10, 18]
print(segment_answers)  # => Output: [5, 7, 10, 18]

assert (
    fenwick_answers == segment_answers  # => both structures agree on every query
)  # => confirms IDENTICAL answers from two structurally different approaches
assert len(fenwick.tree) == n + 1  # => confirms Fenwick's O(n) space usage
assert len(segment_tree.tree) == 4 * n  # => confirms segment tree's larger O(4n) space
print("ex-67 OK")  # => Output: ex-67 OK
