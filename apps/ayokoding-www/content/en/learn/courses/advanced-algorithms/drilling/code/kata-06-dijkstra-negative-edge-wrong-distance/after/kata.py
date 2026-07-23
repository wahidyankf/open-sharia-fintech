"""Kata 6 (after): Bellman-Ford relaxes every edge repeatedly -- no finalization, so negative edges are handled correctly."""

import math


def bellman_ford(
    graph: dict[str, list[tuple[str, int]]], source: str
) -> dict[str, float]:
    dist: dict[str, float] = {node: math.inf for node in graph}
    dist[source] = 0
    for _ in range(
        len(graph) - 1
    ):  # => relax every edge |V| - 1 times -- no node is ever "finalized" early
        for node, edges in graph.items():
            if dist[node] == math.inf:
                continue
            for neighbor, weight in edges:
                if dist[node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[node] + weight
    return dist


graph = {"s": [("b", 1), ("a", 4)], "a": [("b", -10)], "b": [("c", 1)], "c": []}
result = bellman_ford(graph, "s")
print(result["c"])
print(result["c"] == -5)
