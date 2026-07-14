"""Example 59: BFS Shortest-Path Length in an Unweighted Graph."""

# BFS's level-by-level nature means the FIRST time a node is reached, it was
# reached by the shortest possible number of edges -- unweighted only (co-21, co-05).
from collections import (
    deque,
)  # => imports the stdlib double-ended queue as the frontier

graph: dict[str, list[str]] = {  # => a 5-node graph, one edge longer than Example 57's
    "a": ["b", "c"],  # => a's neighbors
    "b": ["a", "d"],  # => b's neighbors
    "c": ["a", "d"],  # => c's neighbors
    "d": ["b", "c", "e"],  # => d's neighbors
    "e": ["d"],  # => e's only neighbor
}  # => five keys total, each mapping to its own neighbor list


# Tracks each node's distance from start, discovered in non-decreasing order via BFS.
def shortest_path_length(graph: dict[str, list[str]], start: str, end: str) -> int:
    distances: dict[str, int] = {start: 0}  # => start is 0 edges from itself
    queue: deque[str] = deque([start])  # => the frontier, FIFO
    while queue:  # => continues until the frontier is empty or end is reached
        node = queue.popleft()  # => O(1): visit the earliest-enqueued node
        if (
            node == end
        ):  # => the FIRST time end is dequeued, its distance is final and minimal
            return distances[node]  # => the shortest number of edges from start to end
        for neighbor in graph[node]:  # => looks at every edge out of this node
            if (
                neighbor not in distances
            ):  # => first discovery -- distance can only get worse later
                distances[neighbor] = (
                    distances[node] + 1
                )  # => one edge farther than node
                queue.append(neighbor)  # => schedules the neighbor for a later visit
    return -1  # => end was never reached -- no path exists (not hit in this example)


distance = shortest_path_length(
    graph, "a", "e"
)  # => a -> b/c (1 edge) -> d (2 edges) -> e (3)
print(distance)  # => Output: 3

assert distance == 3  # => confirms the shortest a-to-e path uses exactly 3 edges
print("ex-59 OK")  # => Output: ex-59 OK
