"""Example 38: Dijkstra's Shortest Paths with a heapq Priority Queue."""

# Dijkstra (co-19) greedily expands the CHEAPEST-known frontier node next,
# using a min-heap (co-09) to find that node in O(log n) instead of an O(n)
# linear scan. Requires NON-NEGATIVE edge weights -- Example 40 shows why.
import heapq  # => the min-heap priority queue used to pick the cheapest frontier node


def dijkstra(  # => greedily finalizes the cheapest-known frontier node each iteration
    graph: dict[str, list[tuple[str, int]]],  # => node -> list of (neighbor, weight)
    start: str,  # => weighted adjacency + origin
) -> dict[str, float]:  # => node -> shortest distance from start
    distances: dict[str, float] = {  # => opens the initial all-infinity distance map
        node: float("inf")  # => every node starts unreachable, by default
        for node in graph  # => every node starts unreachable
    }  # => everyone starts at infinity
    distances[start] = 0  # => the start node is trivially 0 away from itself
    heap: list[
        tuple[float, str]  # => (distance, node) pairs, ordered by distance
    ] = [  # => opens the initial single-entry priority queue
        (0, start)  # => the only known reachable node at distance 0
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
    "a": [("b", 4), ("c", 1)],  # => a's direct routes: to b (cost 4), to c (cost 1)
    "b": [("d", 1)],  # => b's only route: to d (cost 1)
    "c": [("b", 2), ("d", 5)],  # => c offers a cheaper detour to b than a's direct edge
    "d": [],  # => the terminal node -- no outgoing edges
}  # => closes the weighted adjacency map -- 4 nodes
distances = dijkstra(graph, "a")  # => shortest distances from "a" to every other node
print(distances)  # => Output: {'a': 0, 'b': 3, 'c': 1, 'd': 4}

assert distances["a"] == 0  # => the start node is 0 away from itself
assert distances["b"] == 3  # => a->c->b (1+2=3) beats the direct a->b edge (cost 4)
assert distances["d"] == 4  # => a->c->b->d (1+2+1=4) is the cheapest route to d
print("ex-38 OK")  # => Output: ex-38 OK
