"""Example 57: Breadth-First Search over a Graph."""

# BFS explores neighbor-by-neighbor, level by level, using a deque as the
# frontier queue and a set to avoid revisiting nodes (co-21, co-05, co-09).
from collections import (
    deque,
)  # => imports the stdlib double-ended queue as the frontier

graph: dict[str, list[str]] = {  # => the same 4-node graph as Example 56
    "a": ["b", "c"],  # => a's neighbors
    "b": ["a", "d"],  # => b's neighbors
    "c": ["a", "d"],  # => c's neighbors
    "d": ["b", "c"],  # => d's neighbors
}  # => four keys total, each mapping to its own neighbor list


# Visits start, then all its neighbors, then all of THEIR unvisited neighbors, ...
def bfs(
    graph: dict[str, list[str]], start: str
) -> list[str]:  # => a plain BFS function
    visited: set[str] = {
        start
    }  # => tracks every node already enqueued -- O(1) membership
    order: list[str] = []  # => records the order nodes are actually VISITED (dequeued)
    queue: deque[str] = deque([start])  # => the frontier, FIFO
    while queue:  # => continues until the frontier is empty
        node = queue.popleft()  # => O(1): visit the earliest-enqueued node
        order.append(node)  # => records the visit
        for neighbor in graph[node]:  # => looks at every edge out of this node
            if neighbor not in visited:  # => O(1) average -- skip already-seen nodes
                visited.add(
                    neighbor
                )  # => mark BEFORE enqueueing to avoid duplicate enqueues
                queue.append(neighbor)  # => schedules the neighbor for a later visit
    return order  # => the full breadth-first visit order


visit_order = bfs(graph, "a")  # => a -> its neighbors b,c -> their unvisited neighbor d
print(visit_order)  # => Output: ['a', 'b', 'c', 'd']

assert visit_order == [
    "a",
    "b",
    "c",
    "d",
]  # => confirms the exact breadth-first visit order
assert len(visit_order) == len(graph)  # => confirms every node was visited exactly once
print("ex-57 OK")  # => Output: ex-57 OK
