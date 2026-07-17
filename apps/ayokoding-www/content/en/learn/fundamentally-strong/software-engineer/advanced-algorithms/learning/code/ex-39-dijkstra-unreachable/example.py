"""Example 39: Dijkstra Reports Infinity for an Unreachable Node -- Never Crashes."""

# Initializing every distance to infinity BEFORE running Dijkstra (co-19)
# means a node that's never relaxed simply keeps its infinite distance --
# there's no special-case branch needed, and no risk of a KeyError or crash.
import heapq


def dijkstra(
    graph: dict[str, list[tuple[str, int]]], start: str
) -> dict[str, float]:  # => identical to Example 38's implementation
    distances: dict[str, float] = {node: float("inf") for node in graph}
    distances[start] = 0
    heap: list[tuple[float, str]] = [(0, start)]
    visited: set[str] = set()
    while heap:
        dist, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    return distances


graph: dict[str, list[tuple[str, int]]] = {  # => "island" has NO incoming edge from "a"
    "a": [("b", 2)],
    "b": [],
    "island": [],  # => completely disconnected from "a"'s component
}
distances = dijkstra(graph, "a")  # => runs Dijkstra from "a"
print(distances["a"])  # => Output: 0
print(distances["b"])  # => Output: 2
print(
    distances["island"]
)  # => Output: inf -- never relaxed, stays at its initial value

assert distances["b"] == 2  # => confirms the reachable node got its correct distance
assert distances["island"] == float(
    "inf"
)  # => confirms the unreachable node reports infinity, not a crash or missing key
assert "island" in distances  # => confirms the key still exists -- no KeyError risk
print("ex-39 OK")  # => Output: ex-39 OK
