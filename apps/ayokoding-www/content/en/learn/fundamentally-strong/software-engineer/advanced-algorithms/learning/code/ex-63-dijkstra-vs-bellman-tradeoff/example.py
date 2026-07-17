"""Example 63: Dijkstra vs Bellman-Ford -- the Speed/Generality Trade, Measured."""

# On the SAME non-negative-weight graph, both algorithms agree on distances
# (co-19, co-20) -- but Dijkstra's heap-driven O((V+E) log V) does far fewer
# edge relaxations than Bellman-Ford's O(V*E) brute-force repetition.
# Bellman-Ford's payoff for that extra work is GENERALITY: it also handles
# negative edges, which would silently break Dijkstra's greedy assumption.
import heapq
import random


def dijkstra_counted(
    graph: dict[int, list[tuple[int, int]]], start: int
) -> tuple[dict[int, float], int]:  # => (distances, relaxation attempts)
    distances: dict[int, float] = {node: float("inf") for node in graph}
    distances[start] = 0
    heap: list[tuple[float, int]] = [(0, start)]
    visited: set[int] = set()
    relaxations = 0  # => counts every edge examined, across the whole run
    while heap:
        dist, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        for neighbor, weight in graph[node]:
            relaxations += 1  # => one relaxation ATTEMPT per edge examined
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    return distances, relaxations


def bellman_ford_counted(
    n: int, edges: list[tuple[int, int, int]], start: int
) -> tuple[list[float], int]:  # => (distances, relaxation attempts)
    dist: list[float] = [float("inf")] * n
    dist[start] = 0
    relaxations = 0  # => counts every edge examined, across ALL n-1 rounds
    for _ in range(n - 1):  # => O(V) full rounds, EVEN once nothing more can improve
        for u, v, w in edges:  # => O(E) edges examined, every single round
            relaxations += 1  # => one relaxation attempt, whether or not it improves
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist, relaxations


random.seed(91)  # => fixed seed -> reproducible graph structure
n = 40  # => 40 nodes, labeled 0..39
edge_list: list[tuple[int, int, int]] = [  # => a moderately dense random graph
    (u, v, random.randint(1, 20)) for u in range(n) for v in range(n) if u != v
][:300]  # => 300 non-negative-weight edges

adjacency: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
for u, v, w in edge_list:  # => builds Dijkstra's adjacency-list representation
    adjacency[u].append((v, w))

dijkstra_distances, dijkstra_relaxations = dijkstra_counted(adjacency, 0)
bellman_distances, bellman_relaxations = bellman_ford_counted(n, edge_list, 0)

print(dijkstra_relaxations < bellman_relaxations)  # => Output: True
matches = all(
    abs(dijkstra_distances[i] - bellman_distances[i]) < 1e-9 for i in range(n)
)  # => both algorithms must AGREE, since edges here are all non-negative
print(matches)  # => Output: True

assert (
    dijkstra_relaxations < bellman_relaxations
)  # => confirms Dijkstra does meaningfully LESS work on this same graph
assert matches  # => confirms both agree exactly when weights are non-negative
print("ex-63 OK")  # => Output: ex-63 OK
