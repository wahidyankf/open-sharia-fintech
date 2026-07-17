"""Example 63: Dijkstra vs Bellman-Ford -- the Speed/Generality Trade, Measured."""

# On the SAME non-negative-weight graph, both algorithms agree on distances
# (co-19, co-20) -- but Dijkstra's heap-driven O((V+E) log V) does far fewer
# edge relaxations than Bellman-Ford's O(V*E) brute-force repetition.
# Bellman-Ford's payoff for that extra work is GENERALITY: it also handles
# negative edges, which would silently break Dijkstra's greedy assumption.
import heapq
import random


def dijkstra_counted(  # => heap-driven: only relaxes edges from the CLOSEST unfinished node
    graph: dict[int, list[tuple[int, int]]],
    start: int,  # => adjacency list + source node
) -> tuple[dict[int, float], int]:  # => (distances, relaxation attempts)
    distances: dict[int, float] = {
        node: float("inf") for node in graph
    }  # => all unreached
    distances[start] = 0  # => the source reaches itself at cost 0
    heap: list[tuple[float, int]] = [
        (0, start)
    ]  # => (distance, node), ordered by distance
    visited: set[int] = set()  # => nodes whose shortest distance is already finalized
    relaxations = 0  # => counts every edge examined, across the whole run
    while heap:  # => keeps going until every reachable node is finalized
        dist, node = heapq.heappop(heap)  # => pops the CLOSEST unfinished node
        if (
            node in visited
        ):  # => a stale heap entry -- already finalized via a shorter path
            continue  # => skip it, no work to redo
        visited.add(node)  # => this node's shortest distance is now final
        for neighbor, weight in graph[node]:  # => only relaxes THIS node's own edges
            relaxations += 1  # => one relaxation ATTEMPT per edge examined
            new_dist = dist + weight  # => the candidate distance via this node
            if (
                new_dist < distances[neighbor]
            ):  # => a strictly shorter path was just found
                distances[neighbor] = new_dist  # => records the improved distance
                heapq.heappush(
                    heap, (new_dist, neighbor)
                )  # => queues it for future expansion
    return distances, relaxations  # => the final shortest distances + total work done


def bellman_ford_counted(  # => brute-force: relaxes EVERY edge, EVERY round, no early exit
    n: int,
    edges: list[tuple[int, int, int]],
    start: int,  # => node count, edge list, source
) -> tuple[list[float], int]:  # => (distances, relaxation attempts)
    dist: list[float] = [float("inf")] * n  # => all nodes start unreached
    dist[start] = 0  # => the source reaches itself at cost 0
    relaxations = 0  # => counts every edge examined, across ALL n-1 rounds
    for _ in range(n - 1):  # => O(V) full rounds, EVEN once nothing more can improve
        for u, v, w in edges:  # => O(E) edges examined, every single round
            relaxations += 1  # => one relaxation attempt, whether or not it improves
            if (
                dist[u] + w < dist[v]
            ):  # => a strictly shorter path via edge (u, v) was found
                dist[v] = dist[u] + w  # => records the improved distance
    return dist, relaxations  # => the final shortest distances + total work done


random.seed(91)  # => fixed seed -> reproducible graph structure
n = 40  # => 40 nodes, labeled 0..39
edge_list: list[tuple[int, int, int]] = [  # => a moderately dense random graph
    (u, v, random.randint(1, 20))
    for u in range(n)
    for v in range(n)
    if u != v  # => random weight
][:300]  # => 300 non-negative-weight edges

adjacency: dict[int, list[tuple[int, int]]] = {
    i: [] for i in range(n)
}  # => empty adjacency lists
for u, v, w in edge_list:  # => builds Dijkstra's adjacency-list representation
    adjacency[u].append((v, w))  # => one directed edge per entry

dijkstra_distances, dijkstra_relaxations = dijkstra_counted(
    adjacency, 0
)  # => heap-driven run
bellman_distances, bellman_relaxations = bellman_ford_counted(
    n, edge_list, 0
)  # => brute-force run

print(dijkstra_relaxations < bellman_relaxations)  # => Output: True
matches = all(  # => opens the pairwise distance-agreement check
    abs(dijkstra_distances[i] - bellman_distances[i]) < 1e-9
    for i in range(n)  # => near-equal
)  # => both algorithms must AGREE, since edges here are all non-negative
print(matches)  # => Output: True

assert (
    dijkstra_relaxations < bellman_relaxations
)  # => confirms Dijkstra does meaningfully LESS work on this same graph
assert matches  # => confirms both agree exactly when weights are non-negative
print("ex-63 OK")  # => Output: ex-63 OK
