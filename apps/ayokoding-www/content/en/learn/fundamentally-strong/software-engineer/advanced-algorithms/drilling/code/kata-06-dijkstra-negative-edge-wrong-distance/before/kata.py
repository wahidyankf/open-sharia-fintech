"""Kata 6 (before): a `visited` set finalizes each node on first pop, silently corrupting downstream distances on a negative edge."""

import heapq
import math


def dijkstra(graph: dict[str, list[tuple[str, int]]], source: str) -> dict[str, float]:
    dist: dict[str, float] = {node: math.inf for node in graph}
    dist[source] = 0
    visited: set[str] = set()
    heap: list[tuple[float, str]] = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(
            node
        )  # BUG: once a node is finalized, it is NEVER reprocessed, even if dist improves later
        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    return dist


# S -> B costs 1 directly; S -> A -> B costs 4 + (-10) = -6, the TRUE shortest -- but B gets finalized
# via the direct edge BEFORE the negative-weight improvement from A ever arrives.
graph = {"s": [("b", 1), ("a", 4)], "a": [("b", -10)], "b": [("c", 1)], "c": []}
result = dijkstra(graph, "s")
print(result["c"])
print(result["c"] == -5)  # TRUE shortest s -> c is s -> a -> b -> c = 4 - 10 + 1 = -5
