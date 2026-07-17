"""Example 19: BFS -- Shortest Hop-Count on an Unweighted Graph."""

# BFS explores level by level using a QUEUE (co-17): every node at distance k
# is discovered before any node at distance k+1, which is exactly what makes
# the FIRST time a node is reached its true shortest hop-count from the start.
from collections import deque  # => O(1) popleft, unlike list.pop(0)'s O(n)


def bfs_distances(
    graph: dict[str, list[str]], start: str
) -> dict[str, int]:  # => node -> fewest hops from start
    distances: dict[str, int] = {start: 0}  # => the start node is 0 hops from itself
    frontier: deque[str] = deque([start])  # => the BFS queue, seeded with start
    while frontier:  # => keeps expanding until nothing new remains to visit
        node = frontier.popleft()  # => O(1): the earliest-discovered undone node
        for neighbor in graph.get(node, []):  # => every direct neighbor of node
            if (
                neighbor not in distances
            ):  # => first time seeing neighbor -- FINAL hop count
                distances[neighbor] = (
                    distances[node] + 1
                )  # => exactly one more than node's own distance
                frontier.append(neighbor)  # => schedules neighbor's own neighbors next
    return distances  # => shortest hop-count to every reachable node


graph: dict[str, list[str]] = {  # => a small unweighted, undirected graph
    "a": ["b", "c"],
    "b": ["a", "d"],
    "c": ["a", "d"],
    "d": ["b", "c", "e"],
    "e": ["d"],
}
distances = bfs_distances(graph, "a")  # => shortest hops from "a" to every other node
print(distances)  # => Output: {'a': 0, 'b': 1, 'c': 1, 'd': 2, 'e': 3}

assert distances["a"] == 0  # => the start is zero hops from itself
assert distances["b"] == 1  # => a direct neighbor is one hop away
assert distances["d"] == 2  # => reached via b or c, either way exactly 2 hops
assert distances["e"] == 3  # => reached only via d, so exactly 3 hops
print("ex-19 OK")  # => Output: ex-19 OK
