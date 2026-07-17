"""Example 40: Bellman-Ford -- Correct Shortest Paths with Negative Edges."""

# Bellman-Ford (co-20) relaxes EVERY edge, V-1 times over -- slower than
# Dijkstra's O((V+E) log V), at O(V*E), but it TOLERATES negative edge
# weights, which would silently give Dijkstra's greedy heap the wrong answer.


def bellman_ford(
    n: int, edges: list[tuple[int, int, int]], start: int
) -> list[float]:  # => edges: (from, to, weight); returns dist[i] for each node
    dist: list[float] = [float("inf")] * n  # => every node starts at infinity
    dist[start] = 0  # => the start node is 0 away from itself
    for _ in range(n - 1):  # => V-1 full passes -- the longest possible SIMPLE path
        for u, v, w in edges:  # => relaxes every edge, every pass
            if dist[u] + w < dist[v]:  # => found a strictly cheaper way to reach v
                dist[v] = dist[u] + w  # => updates v's distance
    return dist  # => shortest distance to every node, correct even with negative edges


n = 5  # => 5 nodes, labeled 0..4
edges: list[tuple[int, int, int]] = [  # => includes a NEGATIVE edge weight (3 -> 2, -6)
    (0, 1, 6),
    (0, 2, 7),
    (1, 2, 8),
    (1, 3, 5),
    (1, 4, -4),
    (2, 3, -3),
    (2, 4, 9),
    (3, 1, -2),
    (4, 3, 7),
    (4, 0, 2),
]
distances = bellman_ford(n, edges, start=0)  # => shortest distances from node 0
print(distances)  # => Output: [0, 2, 7, 4, -2]

assert distances[0] == 0  # => the start node is 0 away from itself
assert (
    distances[1] == 2
)  # => reached via 0->2->3->1 (7-3-2=2), beats the direct edge (6)
assert distances[4] == -2  # => the negative edge 1->4 pulls this distance below zero
# => a negative-weight EDGE (like 1->4 at -4) doesn't imply a negative CYCLE --
# => Bellman-Ford handles this correctly; Example 41 is what a real cycle looks like
print("ex-40 OK")  # => Output: ex-40 OK
