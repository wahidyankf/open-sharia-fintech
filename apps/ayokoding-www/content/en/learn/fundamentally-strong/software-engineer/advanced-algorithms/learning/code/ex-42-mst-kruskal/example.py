"""Example 42: Kruskal's Minimum Spanning Tree, via Sorting + Union-Find."""

# Kruskal's algorithm (co-21) is GREEDY on edges: sort every edge by weight,
# then add each one UNLESS it would create a cycle -- union-find (co-16)
# answers "would this create a cycle?" in near-constant time via connected().


class UnionFind:  # => the optimized version from Example 33
    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))
        self.rank: list[int] = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(
        self, a: int, b: int
    ) -> bool:  # => returns True if a merge actually happened
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:  # => already connected -- adding this edge would cycle
            return False  # => signals "do not add this edge"
        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1
        return True  # => signals "this edge was safely added"


def kruskal_mst(
    n: int, edges: list[tuple[int, int, int]]
) -> tuple[list[tuple[int, int, int]], int]:  # => (MST edges, total weight)
    sorted_edges = sorted(
        edges, key=lambda e: e[2]
    )  # => O(E log E): cheapest edges first
    uf = UnionFind(n)  # => starts with n singleton components
    mst_edges: list[tuple[int, int, int]] = []  # => accumulates the chosen edges
    total_weight = 0  # => running sum of the MST's edge weights
    for u, v, w in sorted_edges:  # => greedily considers cheapest-first
        if uf.union(u, v):  # => only True if u and v were NOT already connected
            mst_edges.append((u, v, w))  # => this edge is safe -- it can't form a cycle
            total_weight += w  # => tallies its weight into the MST total
    return mst_edges, total_weight  # => the MST's edges and its total weight


n = 5  # => 5 nodes, labeled 0..4
edges: list[tuple[int, int, int]] = [  # => (u, v, weight)
    (0, 1, 2),
    (0, 3, 6),
    (1, 2, 3),
    (1, 3, 8),
    (1, 4, 5),
    (2, 4, 7),
    (3, 4, 9),
]
mst_edges, total_weight = kruskal_mst(n, edges)  # => builds the minimum spanning tree
print(len(mst_edges))  # => Output: 4 -- an MST always has exactly n-1 edges
print(total_weight)  # => Output: 16

assert len(mst_edges) == n - 1  # => confirms exactly n-1 edges -- a spanning tree
assert total_weight == 16  # => confirms the minimum possible total weight
print("ex-42 OK")  # => Output: ex-42 OK
