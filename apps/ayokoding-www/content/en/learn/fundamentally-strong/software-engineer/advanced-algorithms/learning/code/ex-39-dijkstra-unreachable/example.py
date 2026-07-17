"""Example 39: Dijkstra Reports Infinity for an Unreachable Node -- Never Crashes."""

# Initializing every distance to infinity BEFORE running Dijkstra (co-19)
# means a node that's never relaxed simply keeps its infinite distance --
# there's no special-case branch needed, and no risk of a KeyError or crash.
import heapq


def dijkstra(  # => identical to Example 38's implementation
    graph: dict[str, list[tuple[str, int]]],
    start: str,  # => weighted adjacency + origin
) -> dict[str, float]:  # => identical to Example 38's implementation
    distances: dict[str, float] = {  # => every node starts unreachable, by design
        node: float("inf")
        for node in graph  # => "island" gets this same sentinel too
    }  # => closes the dict-comprehension
    distances[start] = 0  # => the start node is trivially 0 away from itself
    heap: list[tuple[float, str]] = [(0, start)]  # => (distance, node) priority queue
    visited: set[str] = set()  # => nodes whose shortest distance is FINAL
    while heap:  # => processes the frontier until nothing remains
        dist, node = heapq.heappop(heap)  # => the currently cheapest unfinalized node
        if node in visited:  # => a stale heap entry -- a shorter path already finalized
            continue  # => skip it, no new information here
        visited.add(node)  # => node's distance is now FINAL -- never improves further
        for neighbor, weight in graph[node]:  # => relaxes every outgoing edge
            new_dist = dist + weight  # => the cost of reaching neighbor THROUGH node
            if new_dist < distances[neighbor]:  # => a strictly better path was found
                distances[neighbor] = new_dist  # => records the improved distance
                heapq.heappush(heap, (new_dist, neighbor))  # => schedules the candidate
    return distances  # => "island" is never touched -- stays at its initial infinity


graph: dict[str, list[tuple[str, int]]] = {  # => "island" has NO incoming edge from "a"
    "a": [("b", 2)],  # => a's only route: to b (cost 2)
    "b": [],  # => a dead end, but still reachable from "a"
    "island": [],  # => completely disconnected from "a"'s component
}  # => closes the adjacency map -- "island" is a member with zero incoming edges
distances = dijkstra(graph, "a")  # => runs Dijkstra from "a"
print(distances["a"])  # => Output: 0
print(distances["b"])  # => Output: 2
print(  # => opens the print call for the unreachable node's distance
    distances["island"]  # => still the original float("inf") sentinel
)  # => Output: inf -- never relaxed, stays at its initial value

assert distances["b"] == 2  # => confirms the reachable node got its correct distance
assert distances["island"] == float(  # => opens the unreachable-node check
    "inf"  # => the exact sentinel value every distance was initialized to
)  # => confirms the unreachable node reports infinity, not a crash or missing key
assert "island" in distances  # => confirms the key still exists -- no KeyError risk
print("ex-39 OK")  # => Output: ex-39 OK
