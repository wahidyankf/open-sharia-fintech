"""Kata 5 (after): Kahn's algorithm checks the output length and raises if a cycle made the DAG assumption false."""

from collections import deque


class CycleError(Exception):
    pass


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

    if len(order) != len(
        graph
    ):  # => the precondition check: a DAG must place EVERY node
        raise CycleError(
            f"graph has a cycle -- only {len(order)}/{len(graph)} nodes reached in-degree 0"
        )
    return order


graph = {"a": ["b"], "b": ["c"], "c": ["a"]}
try:
    topo_sort(graph)
except CycleError as error:
    print(error)
