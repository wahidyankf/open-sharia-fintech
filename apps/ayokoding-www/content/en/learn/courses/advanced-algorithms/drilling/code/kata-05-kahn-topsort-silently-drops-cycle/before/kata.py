"""Kata 5 (before): Kahn's algorithm returns a SHORT, silently-incomplete order for a cyclic graph."""

from collections import deque


def topo_sort(graph: dict[str, list[str]]) -> list[str]:
    in_degree: dict[str, int] = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue: deque[str] = deque(node for node in graph if in_degree[node] == 0)
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order  # BUG: never checks len(order) == len(graph) -- a cycle just produces a short, wrong list


graph = {
    "a": ["b"],
    "b": ["c"],
    "c": ["a"],
}  # a -> b -> c -> a is a cycle: no valid topological order exists
order = topo_sort(graph)
print(order)
print(
    len(order) == len(graph)
)  # a caller trusting `order` with no length check gets a SILENTLY wrong result
