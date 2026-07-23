"""Example 40: Bellman-Ford -- Correct Shortest Paths with Negative Edges."""

# Bellman-Ford (co-20) relaxes EVERY edge, V-1 times over -- slower than
# Dijkstra's O((V+E) log V), at O(V*E), but it TOLERATES negative edge
# weights, which would silently give Dijkstra's greedy heap the wrong answer.


def bellman_ford(  # => brute-force relax-every-edge, repeated V-1 times, no heap needed
    n: int,  # => the number of nodes, labeled 0..n-1
    edges: list[
        tuple[int, int, int]  # => each edge is a (from, to, weight) triple
    ],  # => (from, to, weight) triples, negatives allowed
    start: int,  # => node count, edges, origin
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
    (0, 1, 6),  # => 0 to 1, cost 6
    (0, 2, 7),  # => 0 to 2, cost 7
    (1, 2, 8),  # => 1 to 2, cost 8
    (1, 3, 5),  # => 1 to 3, cost 5
    (
        1,  # => the edge's source node
        4,  # => the edge's destination node
        -4,  # => the negative weight itself
    ),  # => 1 to 4, a NEGATIVE edge -- Dijkstra could not handle this correctly
    (2, 3, -3),  # => 2 to 3, another negative edge
    (2, 4, 9),  # => 2 to 4, cost 9
    (3, 1, -2),  # => 3 to 1, a negative edge feeding back into an earlier node
    (4, 3, 7),  # => 4 to 3, cost 7
    (4, 0, 2),  # => 4 to 0, closes a cycle back to the start -- but NOT a negative one
]  # => closes the edge list -- 10 directed edges, 3 of them negative-weight
distances = bellman_ford(n, edges, start=0)  # => shortest distances from node 0
print(distances)  # => Output: [0, 2, 7, 4, -2]

assert distances[0] == 0  # => the start node is 0 away from itself
assert (  # => opens the "cheaper indirect path wins" check
    distances[1] == 2
)  # => reached via 0->2->3->1 (7-3-2=2), beats the direct edge (6)
assert distances[4] == -2  # => the negative edge 1->4 pulls this distance below zero
# => a negative-weight EDGE (like 1->4 at -4) doesn't imply a negative CYCLE --
# => Bellman-Ford handles this correctly; Example 41 is what a real cycle looks like
print("ex-40 OK")  # => Output: ex-40 OK
