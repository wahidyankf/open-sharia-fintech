"""Example 34: Count Connected Components via Union-Find."""

# Union every edge's two endpoints (co-16), and each surviving DISTINCT root
# afterward identifies one connected component -- no traversal needed at all,
# just a pass over the edges followed by counting unique find() results.


class UnionFind:  # => the optimized version from Example 33, reused as-is
    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))
        self.rank: list[int] = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return
        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1


def count_components(
    n: int, edges: list[tuple[int, int]]
) -> int:  # => O((V+E) alpha(V))
    uf = UnionFind(n)  # => n nodes, each initially its own component
    for a, b in edges:  # => O(E): unions every edge's endpoints
        uf.union(a, b)  # => merges a's and b's components, if not already merged
    roots = {
        uf.find(x) for x in range(n)
    }  # => O(V): the set of DISTINCT surviving roots
    return len(roots)  # => one component per distinct root


n = 8  # => 8 nodes, labeled 0..7
edges: list[tuple[int, int]] = [
    (0, 1),
    (1, 2),
    (3, 4),
    (5, 6),
]  # => leaves 7 fully isolated
component_count = count_components(n, edges)  # => how many separate groups exist
print(component_count)  # => Output: 4 -- {0,1,2}, {3,4}, {5,6}, {7}

assert component_count == 4  # => confirms the four expected groups
assert count_components(5, []) == 5  # => no edges at all: every node is its own group
assert count_components(3, [(0, 1), (1, 2)]) == 1  # => a fully connected chain
print("ex-34 OK")  # => Output: ex-34 OK
