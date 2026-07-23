"""Example 34: Count Connected Components via Union-Find."""

# Union every edge's two endpoints (co-16), and each surviving DISTINCT root
# afterward identifies one connected component -- no traversal needed at all,
# just a pass over the edges followed by counting unique find() results.


class UnionFind:  # => the optimized version from Example 33, reused as-is
    def __init__(self, n: int) -> None:  # => n singleton groups, each its own root
        self.parent: list[int] = list(  # => opens the initial parent-array construction
            range(n)  # => index i's parent starts as i itself -- n separate groups
        )  # => each element starts as its own root
        self.rank: list[int] = [0] * n  # => an upper bound on each tree's height

    def find(self, x: int) -> int:  # => amortized O(alpha(n)) with path compression
        if self.parent[x] != x:  # => x is not yet its own group's root
            self.parent[x] = (
                self.find(  # => recurses first, THEN repoints on the way back
                    self.parent[
                        x  # => the element whose root is being sought
                    ]  # => climbs toward the root through x's current parent
                )  # => closes the recursive find() call
            )  # => path-compresses on the way back
        return self.parent[x]  # => x's parent is now either itself, or the true root

    def union(self, a: int, b: int) -> None:  # => amortized O(alpha(n))
        root_a, root_b = self.find(a), self.find(b)  # => both groups' roots, compressed
        if root_a == root_b:  # => already the same group -- nothing to merge
            return  # => a union with itself is a no-op
        if (  # => opens the shorter-under-taller rank comparison
            self.rank[root_a] < self.rank[root_b]  # => a's tree is strictly shorter
        ):  # => UNION BY RANK: shorter under taller
            self.parent[root_a] = (  # => opens the shorter-under-taller reassignment
                root_b  # => attaches the shorter tree under the taller
            )  # => closes the reassignment
        elif self.rank[root_a] > self.rank[root_b]:  # => the mirror comparison
            self.parent[root_b] = root_a  # => the mirror case
        else:  # => equal rank -- pick either, and the result grows one level taller
            self.parent[root_b] = root_a  # => arbitrarily attaches b's root under a's
            self.rank[root_a] += 1  # => only NOW does the resulting tree's height grow


def count_components(  # => no traversal at all -- just union every edge, then count roots
    n: int,  # => the number of nodes, labeled 0..n-1
    edges: list[tuple[int, int]],  # => n nodes labeled 0..n-1, plus the edge list
) -> int:  # => O((V+E) alpha(V))
    uf = UnionFind(n)  # => n nodes, each initially its own component
    for a, b in edges:  # => O(E): unions every edge's endpoints
        uf.union(a, b)  # => merges a's and b's components, if not already merged
    roots = {  # => opens the set-comprehension collecting distinct roots
        uf.find(x)  # => the compressed root of node x
        for x in range(n)  # => a set automatically discards duplicate roots
    }  # => O(V): the set of DISTINCT surviving roots
    return len(roots)  # => one component per distinct root


n = 8  # => 8 nodes, labeled 0..7
edges: list[  # => opens the edge-list type annotation
    tuple[int, int]  # => each edge is a pair of node indices
] = [  # => opens the edge list -- deliberately leaves node 7 isolated
    (0, 1),  # => connects 0 and 1 into one group
    (1, 2),  # => extends that group to include 2 -- {0, 1, 2}
    (3, 4),  # => a separate two-node group -- {3, 4}
    (5, 6),  # => another separate two-node group -- {5, 6}
]  # => leaves 7 fully isolated
component_count = count_components(n, edges)  # => how many separate groups exist
print(component_count)  # => Output: 4 -- {0,1,2}, {3,4}, {5,6}, {7}

assert component_count == 4  # => confirms the four expected groups
assert count_components(5, []) == 5  # => no edges at all: every node is its own group
assert count_components(3, [(0, 1), (1, 2)]) == 1  # => a fully connected chain
print("ex-34 OK")  # => Output: ex-34 OK
