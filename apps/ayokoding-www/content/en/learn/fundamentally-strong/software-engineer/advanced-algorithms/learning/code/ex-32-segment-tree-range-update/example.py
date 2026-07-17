"""Example 32: Segment Tree with Lazy Range-Add -- O(log n) Range Update, Point Read."""

# A plain segment tree's range update is O(n) (touch every leaf). LAZY
# propagation (co-15) defers that work: a fully-covered node just stamps a
# pending "add" tag and stops -- the tag only gets PUSHED DOWN to children
# when a later query actually needs to look inside that node. O(log n) both ways.


class LazySegmentTree:  # => sum-tracking tree with O(log n) range-add, point query
    def __init__(self, data: list[int]) -> None:
        self.n = len(data)  # => number of leaf elements
        self.tree: list[int] = [0] * (4 * self.n)  # => tree[node] = sum over its range
        self.lazy: list[int] = [0] * (4 * self.n)  # => pending, not-yet-pushed adds
        self._build(data, 1, 0, self.n - 1)  # => builds the initial tree, O(n)

    def _build(self, data: list[int], node: int, lo: int, hi: int) -> None:
        if lo == hi:  # => leaf: exactly one element
            self.tree[node] = data[lo]  # => its own starting value
            return
        mid = (lo + hi) // 2  # => splits the range
        self._build(data, 2 * node, lo, mid)  # => builds the left child
        self._build(data, 2 * node + 1, mid + 1, hi)  # => builds the right child
        self.tree[node] = (
            self.tree[2 * node] + self.tree[2 * node + 1]
        )  # => this node's sum is its children's combined sum

    def _push_down(
        self, node: int, lo: int, hi: int
    ) -> None:  # => flushes a pending tag
        if self.lazy[node] == 0:  # => nothing pending -- nothing to push
            return
        mid = (lo + hi) // 2  # => needed to size each child's range
        for child, child_lo, child_hi in (
            (2 * node, lo, mid),
            (2 * node + 1, mid + 1, hi),
        ):  # => applies the SAME pending delta to both children
            self.tree[child] += self.lazy[node] * (
                child_hi - child_lo + 1
            )  # => scales by range SIZE, since tree[] stores a SUM, not a single value
            self.lazy[child] += self.lazy[node]  # => the child inherits the pending tag
        self.lazy[node] = 0  # => this node's tag has now been fully passed down

    def range_add(
        self, lo: int, hi: int, delta: int
    ) -> None:  # => O(log n): adds delta
        self._range_add(1, 0, self.n - 1, lo, hi, delta)  # => starts at the root

    def _range_add(
        self, node: int, node_lo: int, node_hi: int, lo: int, hi: int, delta: int
    ) -> None:
        if hi < node_lo or node_hi < lo:  # => this node's range is entirely outside
            return  # => nothing to do here
        if lo <= node_lo and node_hi <= hi:  # => this node's range is entirely inside
            self.tree[node] += delta * (
                node_hi - node_lo + 1
            )  # => updates the aggregate sum directly
            self.lazy[node] += delta  # => defers pushing to children until needed
            return  # => THE LAZY PART: children are not touched yet
        self._push_down(
            node, node_lo, node_hi
        )  # => must resolve any pending tag before recursing further
        mid = (node_lo + node_hi) // 2
        self._range_add(2 * node, node_lo, mid, lo, hi, delta)
        self._range_add(2 * node + 1, mid + 1, node_hi, lo, hi, delta)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]  # => recombines

    def point_query(self, i: int) -> int:  # => O(log n): the CURRENT value at index i
        return self._point_query(1, 0, self.n - 1, i)  # => starts at the root

    def _point_query(self, node: int, lo: int, hi: int, i: int) -> int:
        if lo == hi:  # => a leaf -- its stored sum IS the single element's value
            return self.tree[node]  # => already reflects every applied range-add
        self._push_down(
            node, lo, hi
        )  # => resolves any pending tag before descending further
        mid = (lo + hi) // 2
        if i <= mid:  # => the target index lives in the left half
            return self._point_query(2 * node, lo, mid, i)
        return self._point_query(2 * node + 1, mid + 1, hi, i)  # => lives in the right


data: list[int] = [1, 2, 3, 4, 5, 6]  # => 6 starting values
tree = LazySegmentTree(data)  # => O(n): builds the initial tree
tree.range_add(1, 4, 10)  # => O(log n): adds 10 to every element in indices [1, 4]

expected: list[int] = [
    1,
    12,
    13,
    14,
    15,
    6,
]  # => the plain-array result of the same range-add, computed by hand
for i in range(len(data)):  # => reads every index back through the tree
    print(f"index {i}: {tree.point_query(i)}")  # => Output: index N: value, per index
    assert tree.point_query(i) == expected[i]  # => confirms each point read is correct

tree.range_add(0, 2, 5)  # => a SECOND, overlapping range-add, to stack lazy tags
expected2: list[int] = [6, 17, 18, 14, 15, 6]  # => reflects both range-adds combined
for i in range(len(data)):  # => re-reads every index after the second update
    assert tree.point_query(i) == expected2[i]  # => confirms overlapping updates stack
print("ex-32 OK")  # => Output: ex-32 OK
