"""Example 63: pytest verification for the Dijkstra vs Bellman-Ford Trade."""

import random

from example import bellman_ford_counted, dijkstra_counted


def test_both_algorithms_agree_on_a_small_graph() -> None:
    edges = [(0, 1, 4), (0, 2, 1), (1, 3, 1), (2, 1, 2), (2, 3, 5)]
    adjacency: dict[int, list[tuple[int, int]]] = {i: [] for i in range(4)}
    for u, v, w in edges:
        adjacency[u].append((v, w))
    dijkstra_distances, _ = dijkstra_counted(adjacency, 0)
    bellman_distances, _ = bellman_ford_counted(4, edges, 0)
    for i in range(4):
        assert abs(dijkstra_distances[i] - bellman_distances[i]) < 1e-9


def test_dijkstra_does_fewer_relaxations_on_a_larger_random_graph() -> None:
    random.seed(2)
    n = 25
    edges = [
        (u, v, random.randint(1, 15)) for u in range(n) for v in range(n) if u != v
    ][:150]
    adjacency: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
    for u, v, w in edges:
        adjacency[u].append((v, w))
    _, dijkstra_relax = dijkstra_counted(adjacency, 0)
    _, bellman_relax = bellman_ford_counted(n, edges, 0)
    assert dijkstra_relax < bellman_relax


# => Run: pytest -- Output: 2 passed
