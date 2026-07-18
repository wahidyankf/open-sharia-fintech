"""Example 42: Kruskal's Minimum Spanning Tree, via Sorting + Union-Find."""

# Kruskal's algorithm (co-21) is GREEDY on edges: sort every edge by weight,
# then add each one UNLESS it would create a cycle -- union-find (co-16)
# answers "would this create a cycle?" in near-constant time via connected().


class UnionFind:  # => the optimized version from Example 33
    def __init__(self, n: int) -> None:  # => n singleton groups, each its own root
        self.parent: list[int] = list(  # => opens the initial parent-list construction
            range(n)  # => index i's parent starts as i itself
        )  # => each element starts as its own root
        self.rank: list[int] = [0] * n  # => an upper bound on each tree's height

    def find(self, x: int) -> int:  # => amortized O(alpha(n)) with path compression
        if self.parent[x] != x:  # => x is not yet its own group's root
            self.parent[x] = (  # => opens the path-compression reassignment
                self.find(  # => recurses first, THEN repoints on the way back
                    self.parent[
                        x  # => the element whose root is being sought
                    ]  # => climbs toward the root through x's current parent
                )  # => closes the recursive find() call
            )  # => path-compresses on the way back
        return self.parent[x]  # => x's parent is now either itself, or the true root

    def union(  # => the cycle test IS the union: a failed union means "would cycle"
        self,  # => the union-find structure being mutated
        a: int,  # => the candidate edge's first endpoint
        b: int,  # => the two nodes this candidate edge would connect
    ) -> bool:  # => returns True if a merge actually happened
        root_a, root_b = self.find(a), self.find(b)  # => both groups' roots, compressed
        if root_a == root_b:  # => already connected -- adding this edge would cycle
            return False  # => signals "do not add this edge"
        if (  # => opens the rank comparison
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
        return True  # => signals "this edge was safely added"


def kruskal_mst(  # => sort-then-greedily-add, skipping any edge that would form a cycle
    n: int,  # => the number of nodes, labeled 0..n-1
    edges: list[tuple[int, int, int]],  # => node count and (u, v, weight) edges
) -> tuple[list[tuple[int, int, int]], int]:  # => (MST edges, total weight)
    sorted_edges = sorted(  # => opens the ascending-by-weight sort
        edges,  # => the raw, unsorted candidate edges
        key=lambda e: e[2],  # => sorts by the weight field only
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
    (0, 1, 2),  # => the single cheapest edge -- picked first, always safe
    (0, 3, 6),  # => a mid-cost edge, picked only if it doesn't close a cycle
    (1, 2, 3),  # => second-cheapest -- picked early
    (1, 3, 8),  # => the most expensive edge -- likely rejected as redundant
    (1, 4, 5),  # => connects the otherwise-isolated node 4
    (  # => opens the alternate, pricier route to node 4
        2,  # => the edge's source node
        4,  # => the edge's destination node
        7,  # => this alternate route's weight
    ),  # => an alternate, pricier route to node 4 -- rejected once 4 is connected
    (3, 4, 9),  # => the second-most expensive edge -- almost certainly rejected
]  # => closes the edge list -- 5 nodes, 7 candidate edges, MST needs exactly 4
mst_edges, total_weight = kruskal_mst(n, edges)  # => builds the minimum spanning tree
print(len(mst_edges))  # => Output: 4 -- an MST always has exactly n-1 edges
print(total_weight)  # => Output: 16

assert len(mst_edges) == n - 1  # => confirms exactly n-1 edges -- a spanning tree
assert total_weight == 16  # => confirms the minimum possible total weight
print("ex-42 OK")  # => Output: ex-42 OK
