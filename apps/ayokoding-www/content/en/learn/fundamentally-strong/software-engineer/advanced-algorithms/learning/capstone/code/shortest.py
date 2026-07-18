"""Capstone: Dijkstra's shortest path over a weighted variant of the workbench graph.

Time/space complexity (n = nodes, e = edges):

- ``dijkstra``: O((n + e) log n) -- every node is pushed/popped from the heap
  at most once per relaxing edge that improves its distance, each push/pop
  O(log n).
"""

from __future__ import annotations

import heapq

WeightedGraph = dict[str, list[tuple[str, int]]]


def dijkstra(graph: WeightedGraph, source: str) -> dict[str, float]:
    """Single-source shortest paths on non-negative weights -- O((n + e) log n).

    Unreachable nodes are reported as `float('inf')`, never omitted and never
    a crash -- exactly what Example 39 taught for a single unreachable node,
    generalized here to the whole graph.
    """
    if source not in graph:  # => O(1): fail loudly on an unknown source, not silently
        raise KeyError(f"source {source!r} is not a node in the graph")
    distances: dict[str, float] = {
        node: float("inf") for node in graph
    }  # => O(n): every node starts "unreached"
    distances[source] = 0.0  # => the source reaches itself at distance 0
    heap: list[tuple[float, str]] = [(0.0, source)]
    visited: set[str] = set()
    while heap:  # => each node finalized (added to visited) at most once
        dist, node = heapq.heappop(
            heap
        )  # => O(log n): always the closest UNfinalized node
        if node in visited:  # => a stale, already-improved-upon heap entry -- skip it
            continue
        visited.add(node)
        for neighbor, weight in graph[
            node
        ]:  # => O(e) total relaxations across the whole run
            if weight < 0:  # => O(1): Dijkstra's non-negative-weight precondition
                raise ValueError(
                    f"dijkstra requires non-negative weights, got {weight} on edge from {node!r}"
                )
            new_dist = dist + weight
            if new_dist < distances[neighbor]:  # => found a STRICTLY shorter path
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))  # => O(log n)
    return distances
