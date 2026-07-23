"""Example 22: Union-Find (Disjoint Set) -- No Optimizations Yet."""

# A disjoint-set structure (co-16) tracks which elements belong to the SAME
# group. This unoptimized version follows parent pointers to a group's root
# on every find(), and union() just attaches one root under another arbitrarily
# -- correct, but Example 33 shows why this can get slow without path help.


class UnionFind:  # => the plain, unoptimized disjoint-set structure
    def __init__(self, n: int) -> None:  # => starts with n singleton groups: 0..n-1
        self.parent: list[int] = list(
            range(n)
        )  # => each element is initially its OWN root

    def find(self, x: int) -> int:  # => walks parent pointers up to x's group root
        while self.parent[x] != x:  # => keeps climbing until reaching a self-parent
            x = self.parent[x]  # => follows the chain one link at a time
        return x  # => the root that identifies x's whole group

    def union(self, a: int, b: int) -> None:  # => merges a's group with b's group
        root_a = self.find(a)  # => a's group root
        root_b = self.find(b)  # => b's group root
        if root_a != root_b:  # => only merge if they're not already the same group
            self.parent[root_a] = root_b  # => attaches a's whole group under b's root

    def connected(self, a: int, b: int) -> bool:  # => same group?
        return self.find(a) == self.find(b)  # => True iff a and b share a root


uf = UnionFind(6)  # => 6 singleton groups: {0}, {1}, {2}, {3}, {4}, {5}
uf.union(0, 1)  # => merges 0 and 1 into one group
uf.union(1, 2)  # => merges that group with 2 -- now {0, 1, 2}
uf.union(3, 4)  # => a SEPARATE group: {3, 4}

print(uf.connected(0, 2))  # => Output: True -- 0 and 2 both ended up in {0, 1, 2}
print(uf.connected(0, 3))  # => Output: False -- {0,1,2} and {3,4} are separate groups
print(uf.connected(3, 4))  # => Output: True
print(uf.connected(4, 5))  # => Output: False -- 5 was never unioned with anything

assert uf.connected(0, 2) is True  # => confirms transitive union: 0-1 and 1-2 -> 0-2
assert uf.connected(0, 3) is False  # => confirms two groups stay genuinely separate
assert uf.connected(5, 5) is True  # => an element is trivially connected to itself
print("ex-22 OK")  # => Output: ex-22 OK
