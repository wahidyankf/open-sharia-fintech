"""Example 33: Union-Find with Union-by-Rank and Path Compression."""

# Two independent optimizations on top of Example 22's plain union-find
# (co-16): UNION-BY-RANK always attaches the shorter tree under the taller
# one, keeping trees flat; PATH COMPRESSION flattens every node visited
# during find() to point directly at the root. Together they give amortized
# O(alpha(n)) per operation -- alpha is the inverse Ackermann function, which
# is under 5 for any n that could ever be represented in memory: effectively
# constant time in practice, though not literally O(1) in the strict sense.


class OptimizedUnionFind:  # => union-find with both classic optimizations applied
    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(
            range(n)
        )  # => each element starts as its own root
        self.rank: list[int] = [0] * n  # => an upper bound on each tree's height

    def find(self, x: int) -> int:  # => amortized O(alpha(n)) with path compression
        if self.parent[x] != x:  # => x is not yet its own group's root
            self.parent[x] = self.find(
                self.parent[x]
            )  # => PATH COMPRESSION: recurses to the root, then repoints x DIRECTLY at it
        return self.parent[x]  # => x's parent is now either itself, or the true root

    def union(self, a: int, b: int) -> None:  # => amortized O(alpha(n))
        root_a = self.find(a)  # => a's group root (path-compressed along the way)
        root_b = self.find(b)  # => b's group root
        if root_a == root_b:  # => already the same group -- nothing to merge
            return
        if (
            self.rank[root_a] < self.rank[root_b]
        ):  # => UNION BY RANK: shorter under taller
            self.parent[root_a] = (
                root_b  # => attaches the shorter tree under the taller
            )
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a  # => the mirror case
        else:  # => equal rank -- pick either, and the result grows one level taller
            self.parent[root_b] = root_a
            self.rank[root_a] += 1  # => only NOW does the resulting tree's height grow


def total_find_depth(
    uf: OptimizedUnionFind, n: int
) -> int:  # => sums parent-hop counts
    total = 0  # => accumulates hops across every element's find()
    for x in range(n):  # => checks every element once
        depth = 0  # => counts hops from x up to its root
        cur = (
            x  # => a local walker, so find()'s own compression isn't re-triggered here
        )
        while (
            uf.parent[cur] != cur
        ):  # => climbs until reaching a self-parent (the root)
            cur = uf.parent[cur]  # => one hop toward the root
            depth += 1  # => tallies this hop
        total += depth  # => adds this element's hop count to the running total
    return total  # => the sum of all n elements' current depths


n = 1000  # => a reasonably large element count, to make near-flat trees visible
uf = OptimizedUnionFind(n)  # => n singleton groups
for i in range(
    n - 1
):  # => chains everything into ONE big group, worst-case union order
    uf.union(i, i + 1)  # => unions consecutive elements, one after another

for x in range(n):  # => forces every element's find() to run and compress its path
    uf.find(x)  # => after this loop, EVERY element points close to directly at the root

average_depth = (
    total_find_depth(uf, n) / n
)  # => average remaining hops after compression
print(average_depth < 3.0)  # => Output: True -- effectively flat, not O(n) deep
print(uf.find(0) == uf.find(n - 1))  # => Output: True -- all n elements are one group

assert (
    average_depth < 3.0
)  # => confirms near-constant depth despite a 1000-element chain
assert uf.find(0) == uf.find(n - 1)  # => confirms the whole chain merged into one group
print("ex-33 OK")  # => Output: ex-33 OK
