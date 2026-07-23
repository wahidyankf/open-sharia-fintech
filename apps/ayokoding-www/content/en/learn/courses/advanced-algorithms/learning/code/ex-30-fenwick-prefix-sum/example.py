"""Example 30: Fenwick Tree (Binary Indexed Tree) -- O(log n) Prefix Sum + Update."""

# A Fenwick tree (co-14) stores partial sums keyed by the LOWEST SET BIT of
# each index -- both point-update and prefix-sum become O(log n), beating a
# plain array's O(n) prefix-sum recompute and a running-array's O(n) update-shift.


class FenwickTree:  # => 1-indexed internally -- index 0 is unused, by convention
    def __init__(self, n: int) -> None:  # => allocates a zeroed tree sized for n items
        self.n = n  # => the number of elements this tree covers
        self.tree: list[int] = [0] * (n + 1)  # => tree[i] holds a partial-sum range

    def update(self, i: int, delta: int) -> None:  # => O(log n): adds delta at index i
        i += 1  # => converts the caller's 0-indexed position to 1-indexed internally
        while i <= self.n:  # => climbs toward the root, following the BIT structure
            self.tree[i] += delta  # => applies delta to this partial-sum node
            i += i & (-i)  # => jumps to the next node this index's range feeds into
            # => `i & (-i)` isolates the lowest set bit -- the core BIT trick

    def prefix_sum(  # => walks DOWN the BIT structure, accumulating partial sums
        self,  # => the tree instance holding this Fenwick array
        i: int,  # => the (0-indexed) inclusive upper bound of the prefix
    ) -> int:  # => O(log n): sum of elements [0, i] inclusive
        i += 1  # => converts to 1-indexed
        total = 0  # => accumulates the running sum
        while i > 0:  # => walks DOWN toward index 0, following the BIT structure
            total += self.tree[i]  # => adds this node's partial sum
            i -= i & (-i)  # => strips the lowest set bit, moving to the parent range
        return total  # => the sum of all elements from index 0 through i, inclusive

    def range_sum(self, lo: int, hi: int) -> int:  # => O(log n): sum of [lo, hi]
        if lo == 0:  # => no need to subtract anything below index 0
            return self.prefix_sum(hi)  # => the prefix sum IS the range sum
        return self.prefix_sum(hi) - self.prefix_sum(  # => two O(log n) lookups
            lo - 1  # => excludes everything strictly below lo
        )  # => classic prefix-sum subtraction trick


values: list[int] = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2]  # => 10 starting values
n = len(values)  # => n = 10
fenwick = FenwickTree(n)  # => starts as all zeros
for idx, v in enumerate(values):  # => O(n log n) total: one update per starting value
    fenwick.update(idx, v)  # => builds up the tree to reflect `values`

running_array = list(values)  # => a plain array, kept in sync for cross-checking
print(fenwick.prefix_sum(4))  # => Output: 15 -- sum of values[0..4]
print(sum(running_array[: 4 + 1]))  # => Output: 15 -- confirms the plain-array sum

fenwick.update(2, 10)  # => adds 10 AT index 2 (a point update, not a set)
running_array[2] += 10  # => keeps the plain array in sync for comparison
print(fenwick.prefix_sum(4))  # => Output: 25 -- 15 + 10, reflecting the point update
print(fenwick.range_sum(3, 7))  # => Output: 15 -- sum of values[3..7] after the update

assert (  # => opens the Fenwick-vs-plain-sum cross-check
    fenwick.prefix_sum(4)
    == sum(  # => cross-checks the Fenwick tree vs a plain sum
        running_array[: 4 + 1]  # => the same [0, 4] slice, summed the naive O(n) way
    )  # => closes the naive prefix sum call
)  # => confirms Fenwick matches a plain re-sum after the update
assert (  # => opens the arbitrary-range cross-check
    fenwick.range_sum(3, 7)
    == sum(  # => cross-checks an arbitrary mid-range sum
        running_array[3 : 7 + 1]  # => the same [3, 7] slice, summed the naive O(n) way
    )  # => closes the naive range sum call
)  # => confirms arbitrary range sums match too
print("ex-30 OK")  # => Output: ex-30 OK
