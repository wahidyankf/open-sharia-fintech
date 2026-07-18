"""Example 33: Union-Find with Union-by-Rank and Path Compression."""

# Two independent optimizations on top of Example 22's plain union-find
# (co-16): UNION-BY-RANK always attaches the shorter tree under the taller
# one, keeping trees flat; PATH COMPRESSION flattens every node visited
# during find() to point directly at the root. Together they give amortized
# O(alpha(n)) per operation -- alpha is the inverse Ackermann function, which
# is under 5 for any n that could ever be represented in memory: effectively
# constant time in practice, though not literally O(1) in the strict sense.


class OptimizedUnionFind:  # => union-find with both classic optimizations applied
    def __init__(self, n: int) -> None:  # => n singleton groups, each its own root
        self.parent: list[int] = list(  # => opens the initial parent-list construction
            range(n)  # => index i's parent starts as i itself -- n separate groups
        )  # => each element starts as its own root
        self.rank: list[int] = [0] * n  # => an upper bound on each tree's height

    def find(self, x: int) -> int:  # => amortized O(alpha(n)) with path compression
        if self.parent[x] != x:  # => x is not yet its own group's root
            self.parent[x] = (
                self.find(  # => recurses first, THEN repoints on the way back
                    self.parent[
                        x
                    ]  # => climbs toward the root through x's current parent
                )  # => closes the recursive find() call
            )  # => PATH COMPRESSION: recurses to the root, then repoints x DIRECTLY at it
        return self.parent[x]  # => x's parent is now either itself, or the true root

    def union(self, a: int, b: int) -> None:  # => amortized O(alpha(n))
        root_a = self.find(a)  # => a's group root (path-compressed along the way)
        root_b = self.find(b)  # => b's group root
        if root_a == root_b:  # => already the same group -- nothing to merge
            return  # => a union with itself is a no-op
        if (  # => opens the rank comparison
            self.rank[root_a] < self.rank[root_b]
        ):  # => UNION BY RANK: shorter under taller
            self.parent[root_a] = (  # => opens the shorter-under-taller reassignment
                root_b  # => attaches the shorter tree under the taller
            )  # => closes the reassignment
        elif self.rank[root_a] > self.rank[root_b]:  # => the mirror comparison
            self.parent[root_b] = root_a  # => the mirror case
        else:  # => equal rank -- pick either, and the result grows one level taller
            self.parent[root_b] = root_a  # => arbitrarily attaches b's root under a's
            self.rank[root_a] += 1  # => only NOW does the resulting tree's height grow


def total_find_depth(  # => a diagnostic helper -- NOT part of the union-find API itself
    uf: OptimizedUnionFind,  # => the union-find structure being queried
    n: int,  # => the structure to measure, and its element count
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


# => margin note: n stays large enough that even O(n) depth would be visible
n = 1000  # => a reasonably large element count, to make near-flat trees visible
uf = OptimizedUnionFind(n)  # => n singleton groups
for i in range(  # => opens the union-count range
    n - 1  # => one union per consecutive pair -- n-1 total union calls
):  # => chains everything into ONE big group, worst-case union order
    uf.union(i, i + 1)  # => unions consecutive elements, one after another

for x in range(n):  # => forces every element's find() to run and compress its path
    uf.find(x)  # => after this loop, EVERY element points close to directly at the root

average_depth = (  # => opens the average-hops-per-element computation
    total_find_depth(uf, n) / n  # => total hops divided by the element count
)  # => average remaining hops after compression
print(average_depth < 3.0)  # => Output: True -- effectively flat, not O(n) deep
print(uf.find(0) == uf.find(n - 1))  # => Output: True -- all n elements are one group

# => without path compression, this 1000-element CHAIN union order would leave average
# => depth near n/2 -- the near-flat result below is entirely due to the optimizations
assert (  # => opens the near-flat-depth check
    average_depth < 3.0  # => True only if the optimizations actually kept trees flat
)  # => confirms near-constant depth despite a 1000-element chain
assert uf.find(0) == uf.find(n - 1)  # => confirms the whole chain merged into one group
print("ex-33 OK")  # => Output: ex-33 OK
