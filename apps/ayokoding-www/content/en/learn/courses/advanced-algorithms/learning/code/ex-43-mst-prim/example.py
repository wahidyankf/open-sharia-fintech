"""Example 43: Prim's Minimum Spanning Tree, via a Heap."""

# Prim's algorithm (co-21) is GREEDY on nodes instead of edges: grow ONE tree
# from a start node, always adding the CHEAPEST edge that connects the
# growing tree to a new node -- a min-heap (co-09) finds that edge in O(log E).
import heapq  # => the min-heap priority queue used to pick the cheapest frontier edge


def prim_mst(  # => grows ONE tree from node 0, always via the cheapest frontier edge
    n: int,  # => the number of nodes, labeled 0..n-1
    adjacency: dict[int, list[tuple[int, int]]],  # => node count + weighted adjacency
) -> tuple[list[tuple[int, int, int]], int]:  # => (MST edges, total weight)
    in_tree: set[int] = {0}  # => the growing tree starts as just node 0
    mst_edges: list[tuple[int, int, int]] = []  # => accumulates (u, v, weight) chosen
    total_weight = 0  # => running sum of the MST's edge weights
    heap: list[tuple[int, int, int]] = [  # => (weight, from_node, to_node) candidates
        (w, 0, v)  # => (weight, from, to) so heapq sorts by weight automatically
        for v, w in adjacency[0]  # => every edge leaving the start node
    ]  # => the initial frontier, before heapify imposes heap order
    heapq.heapify(heap)  # => O(E): arranges the initial candidate edges into heap order
    while len(in_tree) < n:  # => stops once every node has joined the tree
        weight, u, v = heapq.heappop(heap)  # => the cheapest candidate edge overall
        if (  # => opens the stale-entry check
            v in in_tree  # => True if v was already added via an earlier, cheaper pop
        ):  # => a stale entry -- v joined the tree via a cheaper edge already
            continue  # => skip it, no new information
        in_tree.add(v)  # => v now joins the growing tree
        mst_edges.append((u, v, weight))  # => this edge is part of the MST
        total_weight += weight  # => tallies its weight
        for neighbor, w in adjacency[v]:  # => v's edges become new candidates
            if (  # => opens the outside-the-tree check
                neighbor not in in_tree  # => True only if neighbor hasn't joined yet
            ):  # => only edges reaching OUTSIDE the tree matter
                heapq.heappush(  # => the heap may end up holding stale entries too
                    heap,  # => the shared candidate-edge priority queue
                    (w, v, neighbor),  # => a new candidate frontier edge
                )  # => schedules this new candidate
    return mst_edges, total_weight  # => the MST's edges and its total weight


adjacency: dict[int, list[tuple[int, int]]] = {  # => the SAME graph as Example 42
    0: [(1, 2), (3, 6)],  # => node 0's two outgoing edges -- the initial frontier
    1: [  # => opens node 1's edge list
        (0, 2),  # => back to node 0
        (2, 3),  # => to node 2
        (3, 8),  # => to node 3, the priciest of node 1's edges
        (4, 5),  # => to node 4
    ],  # => node 1's edges, including the priciest one
    2: [(1, 3), (4, 7)],  # => node 2's two edges
    3: [  # => opens node 3's edge list
        (0, 6),  # => back to node 0
        (1, 8),  # => to node 1, tied for priciest overall
        (4, 9),  # => to node 4, the single priciest edge overall
    ],  # => node 3's edges, including the two priciest overall
    4: [(1, 5), (2, 7), (3, 9)],  # => node 4's edges
}  # => closes the adjacency map -- an undirected graph, each edge listed from both ends

mst_edges, total_weight = prim_mst(5, adjacency)  # => builds the MST, starting from 0
print(len(mst_edges))  # => Output: 4
print(total_weight)  # => Output: 16 -- matches Kruskal's answer on the same graph

assert len(mst_edges) == 4  # => confirms exactly n-1 edges
assert total_weight == 16  # => confirms the SAME minimum weight as Example 42's Kruskal
print("ex-43 OK")  # => Output: ex-43 OK
