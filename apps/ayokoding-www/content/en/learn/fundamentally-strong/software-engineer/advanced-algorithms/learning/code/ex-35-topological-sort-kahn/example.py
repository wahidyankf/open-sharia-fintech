"""Example 35: Topological Sort via Kahn's Algorithm."""

# Kahn's algorithm (co-18) repeatedly removes nodes with IN-DEGREE ZERO --
# nodes with no remaining unprocessed prerequisites -- appending each to the
# result and decrementing its neighbors' in-degrees, until none remain.
from collections import deque


def kahn_topological_sort(
    graph: dict[str, list[str]],
) -> list[str] | None:  # => None if a cycle makes ordering impossible
    in_degree: dict[str, int] = {
        node: 0 for node in graph
    }  # => starts every node's in-degree at 0
    for node in graph:  # => O(V+E): counts how many edges point INTO each node
        for neighbor in graph[node]:
            in_degree[neighbor] += 1  # => one more prerequisite for neighbor

    queue: deque[str] = deque(
        [node for node in graph if in_degree[node] == 0]
    )  # => nodes with NO prerequisites can go first
    order: list[str] = []  # => accumulates the resulting topological order
    while queue:  # => processes nodes in waves of "everything now unblocked"
        node = queue.popleft()  # => O(1): the next ready node
        order.append(node)  # => it has no remaining unprocessed prerequisites
        for neighbor in graph[node]:  # => "removes" node by decrementing its neighbors
            in_degree[neighbor] -= 1  # => one fewer prerequisite for neighbor
            if in_degree[neighbor] == 0:  # => neighbor is now fully unblocked
                queue.append(neighbor)  # => schedules it for the next wave

    if len(order) != len(graph):  # => fewer nodes than expected means a CYCLE exists
        return None  # => a cycle prevents any valid topological order
    return order  # => a valid topological order: every edge points forward in the list


graph: dict[str, list[str]] = {  # => a small build-dependency DAG
    "compile": ["link"],
    "link": ["test"],
    "fetch_deps": ["compile"],
    "test": [],
}
order = kahn_topological_sort(graph)  # => a valid build order
print(order)  # => Output: ['fetch_deps', 'compile', 'link', 'test']

assert order is not None  # => confirms no cycle was detected
position = {
    node: i for i, node in enumerate(order)
}  # => node -> its index in the order
assert position["fetch_deps"] < position["compile"]  # => a dependency comes first
assert position["compile"] < position["link"]  # => confirms edge direction is honored
assert position["link"] < position["test"]  # => confirms the last edge too
print("ex-35 OK")  # => Output: ex-35 OK
