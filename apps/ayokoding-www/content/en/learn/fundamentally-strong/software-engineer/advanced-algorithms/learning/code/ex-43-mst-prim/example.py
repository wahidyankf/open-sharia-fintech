"""Example 43: Prim's Minimum Spanning Tree, via a Heap."""

# Prim's algorithm (co-21) is GREEDY on nodes instead of edges: grow ONE tree
# from a start node, always adding the CHEAPEST edge that connects the
# growing tree to a new node -- a min-heap (co-09) finds that edge in O(log E).
import heapq


def prim_mst(
    n: int, adjacency: dict[int, list[tuple[int, int]]]
) -> tuple[list[tuple[int, int, int]], int]:  # => (MST edges, total weight)
    in_tree: set[int] = {0}  # => the growing tree starts as just node 0
    mst_edges: list[tuple[int, int, int]] = []  # => accumulates (u, v, weight) chosen
    total_weight = 0  # => running sum of the MST's edge weights
    heap: list[tuple[int, int, int]] = [  # => (weight, from_node, to_node) candidates
        (w, 0, v) for v, w in adjacency[0]
    ]
    heapq.heapify(heap)  # => O(E): arranges the initial candidate edges into heap order
    while len(in_tree) < n:  # => stops once every node has joined the tree
        weight, u, v = heapq.heappop(heap)  # => the cheapest candidate edge overall
        if (
            v in in_tree
        ):  # => a stale entry -- v joined the tree via a cheaper edge already
            continue  # => skip it, no new information
        in_tree.add(v)  # => v now joins the growing tree
        mst_edges.append((u, v, weight))  # => this edge is part of the MST
        total_weight += weight  # => tallies its weight
        for neighbor, w in adjacency[v]:  # => v's edges become new candidates
            if (
                neighbor not in in_tree
            ):  # => only edges reaching OUTSIDE the tree matter
                heapq.heappush(
                    heap, (w, v, neighbor)
                )  # => schedules this new candidate
    return mst_edges, total_weight  # => the MST's edges and its total weight


adjacency: dict[int, list[tuple[int, int]]] = {  # => the SAME graph as Example 42
    0: [(1, 2), (3, 6)],
    1: [(0, 2), (2, 3), (3, 8), (4, 5)],
    2: [(1, 3), (4, 7)],
    3: [(0, 6), (1, 8), (4, 9)],
    4: [(1, 5), (2, 7), (3, 9)],
}
mst_edges, total_weight = prim_mst(5, adjacency)  # => builds the MST, starting from 0
print(len(mst_edges))  # => Output: 4
print(total_weight)  # => Output: 16 -- matches Kruskal's answer on the same graph

assert len(mst_edges) == 4  # => confirms exactly n-1 edges
assert total_weight == 16  # => confirms the SAME minimum weight as Example 42's Kruskal
print("ex-43 OK")  # => Output: ex-43 OK
