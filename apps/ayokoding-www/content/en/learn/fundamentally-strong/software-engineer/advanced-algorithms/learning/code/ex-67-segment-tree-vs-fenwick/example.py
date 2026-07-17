"""Example 67: Segment Tree vs Fenwick Tree -- Same Prefix-Sum Answers, Different Cost."""

# Both structures answer prefix-sum + point-update in O(log n) (co-14,
# co-15) -- but a Fenwick tree needs only O(n) space and a handful of lines
# (Example 30), while a segment tree needs O(4n) space and more code, in
# exchange for handling queries a Fenwick tree CAN'T (like range-min).


class FenwickTree:  # => identical to Example 30's implementation
    def __init__(self, n: int) -> None:
        self.n = n
        self.tree: list[int] = [0] * (n + 1)  # => O(n) space -- a single flat array

    def update(self, i: int, delta: int) -> None:
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def prefix_sum(self, i: int) -> int:
        i += 1
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)
        return total


class SegmentTreeSum:  # => a sum-tracking segment tree -- more code, more memory
    def __init__(self, n: int) -> None:
        self.n = n
        self.tree: list[int] = [0] * (
            4 * n
        )  # => O(4n) space -- 4x a Fenwick tree's array

    def update(self, i: int, delta: int) -> None:
        self._update(1, 0, self.n - 1, i, delta)

    def _update(self, node: int, lo: int, hi: int, i: int, delta: int) -> None:
        if lo == hi:
            self.tree[node] += delta
            return
        mid = (lo + hi) // 2
        if i <= mid:
            self._update(2 * node, lo, mid, i, delta)
        else:
            self._update(2 * node + 1, mid + 1, hi, i, delta)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def prefix_sum(self, i: int) -> int:  # => needs its OWN range-query traversal
        return self._query(1, 0, self.n - 1, 0, i)

    def _query(self, node: int, node_lo: int, node_hi: int, lo: int, hi: int) -> int:
        if hi < node_lo or node_hi < lo:
            return 0
        if lo <= node_lo and node_hi <= hi:
            return self.tree[node]
        mid = (node_lo + node_hi) // 2
        return self._query(2 * node, node_lo, mid, lo, hi) + self._query(
            2 * node + 1, mid + 1, node_hi, lo, hi
        )


n = 12  # => 12 elements, both starting at zero
fenwick = FenwickTree(n)
segment_tree = SegmentTreeSum(n)
updates: list[tuple[int, int]] = [
    (0, 5),
    (3, 2),
    (7, -1),
    (11, 8),
    (5, 4),
]  # => the SAME sequence of point updates, applied to BOTH structures
for idx, delta in updates:
    fenwick.update(idx, delta)  # => O(log n): a handful of pointer-arithmetic hops
    segment_tree.update(idx, delta)  # => O(log n): a recursive tree descent

queries: list[int] = [0, 3, 7, 11]  # => a spread of prefix-sum queries to compare
fenwick_answers = [fenwick.prefix_sum(i) for i in queries]
segment_answers = [segment_tree.prefix_sum(i) for i in queries]
print(fenwick_answers)  # => Output: [5, 7, 10, 18]
print(segment_answers)  # => Output: [5, 7, 10, 18]

assert (
    fenwick_answers == segment_answers
)  # => confirms IDENTICAL answers from two structurally different approaches
assert len(fenwick.tree) == n + 1  # => confirms Fenwick's O(n) space usage
assert len(segment_tree.tree) == 4 * n  # => confirms segment tree's larger O(4n) space
print("ex-67 OK")  # => Output: ex-67 OK
