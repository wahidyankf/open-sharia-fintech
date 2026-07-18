"""Example 32: Segment Tree with Lazy Range-Add -- O(log n) Range Update, Point Read."""

# A plain segment tree's range update is O(n) (touch every leaf). LAZY
# propagation (co-15) defers that work: a fully-covered node just stamps a
# pending "add" tag and stops -- the tag only gets PUSHED DOWN to children
# when a later query actually needs to look inside that node. O(log n) both ways.


class LazySegmentTree:  # => sum-tracking tree with O(log n) range-add, point query
    def __init__(self, data: list[int]) -> None:  # => O(n): builds the initial tree
        self.n = len(data)  # => number of leaf elements
        self.tree: list[int] = [0] * (4 * self.n)  # => tree[node] = sum over its range
        self.lazy: list[int] = [0] * (4 * self.n)  # => pending, not-yet-pushed adds
        self._build(data, 1, 0, self.n - 1)  # => builds the initial tree, O(n)

    def _build(  # => bottom-up: leaves first, then each parent sums its two children
        self,  # => the tree instance under construction
        data: list[int],  # => the source array being indexed
        node: int,  # => this call's own array-backed tree index
        lo: int,  # => the low end of this node's range
        hi: int,  # => [lo, hi] is this node's range
    ) -> None:  # => fills self.tree over the array-index encoding, no lazy tags yet
        if lo == hi:  # => leaf: exactly one element
            self.tree[node] = data[lo]  # => its own starting value
            return  # => nothing more to combine at a leaf
        mid = (lo + hi) // 2  # => splits the range
        self._build(data, 2 * node, lo, mid)  # => builds the left child
        self._build(data, 2 * node + 1, mid + 1, hi)  # => builds the right child
        self.tree[node] = (  # => opens the parent-sum assignment
            self.tree[2 * node]  # => the left child's own sum
            + self.tree[2 * node + 1]  # => plus the right child's own sum
        )  # => this node's sum is its children's combined sum

    def _push_down(  # => flushes node's pending tag one level down, THEN clears it
        self,  # => the tree instance being flushed
        node: int,  # => this call's own array-backed tree index
        lo: int,  # => the low end of this node's range
        hi: int,  # => node's own [lo, hi] range
    ) -> None:  # => flushes a pending tag
        if self.lazy[node] == 0:  # => nothing pending -- nothing to push
            return  # => an early exit avoids touching children unnecessarily
        mid = (lo + hi) // 2  # => needed to size each child's range
        for child, child_lo, child_hi in (  # => opens the (index, lo, hi) pair loop
            (2 * node, lo, mid),  # => the left child's index and range
            (2 * node + 1, mid + 1, hi),  # => the right child's index and range
        ):  # => applies the SAME pending delta to both children
            self.tree[child] += self.lazy[node] * (  # => scales the delta by range size
                child_hi - child_lo + 1  # => how many elements this child's range spans
            )  # => scales by range SIZE, since tree[] stores a SUM, not a single value
            self.lazy[child] += self.lazy[node]  # => the child inherits the pending tag
        self.lazy[node] = 0  # => this node's tag has now been fully passed down

    def range_add(  # => public entry point -- the only method callers use to update
        self,  # => the tree instance being updated
        lo: int,  # => the low end of the range to add to
        hi: int,  # => the high end of the range to add to
        delta: int,  # => adds delta to every index in [lo, hi]
    ) -> None:  # => O(log n): adds delta
        self._range_add(1, 0, self.n - 1, lo, hi, delta)  # => starts at the root

    def _range_add(  # => the classic outside/inside/partial-overlap recursive split
        self,  # => the tree instance being updated
        node: int,  # => this call's own array-backed tree index
        node_lo: int,  # => this node's range's low end
        node_hi: int,  # => this node's range's high end
        lo: int,  # => the update range's low end
        hi: int,  # => the update range's high end
        delta: int,  # => node covers [node_lo, node_hi]
    ) -> None:  # => mutates self.tree and self.lazy in place, returns nothing
        if hi < node_lo or node_hi < lo:  # => this node's range is entirely outside
            return  # => nothing to do here
        if lo <= node_lo and node_hi <= hi:  # => this node's range is entirely inside
            self.tree[node] += delta * (  # => the aggregate sum shifts by delta * count
                node_hi - node_lo + 1  # => how many elements this whole node covers
            )  # => updates the aggregate sum directly
            self.lazy[node] += delta  # => defers pushing to children until needed
            return  # => THE LAZY PART: children are not touched yet
        self._push_down(  # => must resolve any pending tag before recursing further
            node,  # => this node's own array-backed tree index
            node_lo,  # => this node's own range low end
            node_hi,  # => flushes THIS node's own stale tag first
        )  # => must resolve any pending tag before recursing further
        mid = (node_lo + node_hi) // 2  # => splits this node's range for the recursion
        self._range_add(2 * node, node_lo, mid, lo, hi, delta)  # => recurses left
        self._range_add(2 * node + 1, mid + 1, node_hi, lo, hi, delta)  # => and right
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]  # => recombines

    def point_query(self, i: int) -> int:  # => O(log n): the CURRENT value at index i
        return self._point_query(1, 0, self.n - 1, i)  # => starts at the root

    def _point_query(  # => descends one side at each level, pushing down tags first
        self,  # => the tree instance being queried
        node: int,  # => this call's own array-backed tree index
        lo: int,  # => this node's range's low end
        hi: int,  # => this node's range's high end
        i: int,  # => node covers [lo, hi]; i is the target
    ) -> int:  # => returns the up-to-date value at index i
        if lo == hi:  # => a leaf -- its stored sum IS the single element's value
            return self.tree[node]  # => already reflects every applied range-add
        self._push_down(  # => resolves any pending tag before descending further
            node,  # => this node's own array-backed tree index
            lo,  # => this node's own range low end
            hi,  # => this node's own range, needed to size its children
        )  # => resolves any pending tag before descending further
        mid = (lo + hi) // 2  # => decides which child holds index i
        if i <= mid:  # => the target index lives in the left half
            return self._point_query(2 * node, lo, mid, i)  # => recurses left
        return self._point_query(2 * node + 1, mid + 1, hi, i)  # => lives in the right


data: list[int] = [1, 2, 3, 4, 5, 6]  # => 6 starting values
tree = LazySegmentTree(data)  # => O(n): builds the initial tree
tree.range_add(1, 4, 10)  # => O(log n): adds 10 to every element in indices [1, 4]

expected: list[int] = [  # => opens the hand-computed plain-array result
    1,  # => index 0 -- outside [1, 4], unchanged
    12,  # => index 1 -- 2 + 10
    13,  # => index 2 -- 3 + 10
    14,  # => index 3 -- 4 + 10
    15,  # => index 4 -- 5 + 10
    6,  # => index 5 -- outside [1, 4], unchanged
]  # => the plain-array result of the same range-add, computed by hand
for i in range(len(data)):  # => reads every index back through the tree
    print(f"index {i}: {tree.point_query(i)}")  # => Output: index N: value, per index
    assert tree.point_query(i) == expected[i]  # => confirms each point read is correct

tree.range_add(0, 2, 5)  # => a SECOND, overlapping range-add, to stack lazy tags
expected2: list[int] = [6, 17, 18, 14, 15, 6]  # => reflects both range-adds combined
for i in range(len(data)):  # => re-reads every index after the second update
    assert tree.point_query(i) == expected2[i]  # => confirms overlapping updates stack
print("ex-32 OK")  # => Output: ex-32 OK
