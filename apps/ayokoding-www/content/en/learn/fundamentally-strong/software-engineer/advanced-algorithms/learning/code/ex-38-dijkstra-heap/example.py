"""Example 38: Dijkstra's Shortest Paths with a heapq Priority Queue."""

# Dijkstra (co-19) greedily expands the CHEAPEST-known frontier node next,
# using a min-heap (co-09) to find that node in O(log n) instead of an O(n)
# linear scan. Requires NON-NEGATIVE edge weights -- Example 40 shows why.
import heapq


def dijkstra(
    graph: dict[str, list[tuple[str, int]]], start: str
) -> dict[str, float]:  # => node -> shortest distance from start
    distances: dict[str, float] = {
        node: float("inf") for node in graph
    }  # => everyone starts at infinity
    distances[start] = 0  # => the start node is trivially 0 away from itself
    heap: list[tuple[float, str]] = [
        (0, start)
    ]  # => (distance, node) -- heapq sorts by distance
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
    return distances  # => shortest distance to every node reachable from start


graph: dict[str, list[tuple[str, int]]] = {  # => node -> list of (neighbor, weight)
    "a": [("b", 4), ("c", 1)],
    "b": [("d", 1)],
    "c": [("b", 2), ("d", 5)],
    "d": [],
}
distances = dijkstra(graph, "a")  # => shortest distances from "a" to every other node
print(distances)  # => Output: {'a': 0, 'b': 3, 'c': 1, 'd': 4}

assert distances["a"] == 0  # => the start node is 0 away from itself
assert distances["b"] == 3  # => a->c->b (1+2=3) beats the direct a->b edge (cost 4)
assert distances["d"] == 4  # => a->c->b->d (1+2+1=4) is the cheapest route to d
print("ex-38 OK")  # => Output: ex-38 OK
