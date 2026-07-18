"""Example 35: Topological Sort via Kahn's Algorithm."""

# Kahn's algorithm (co-18) repeatedly removes nodes with IN-DEGREE ZERO --
# nodes with no remaining unprocessed prerequisites -- appending each to the
# result and decrementing its neighbors' in-degrees, until none remain.
from collections import deque  # => O(1) popleft, unlike a plain list


def kahn_topological_sort(  # => BFS-style: repeatedly peel off zero-in-degree nodes
    graph: dict[str, list[str]],  # => adjacency map: node -> list of nodes it points to
) -> list[str] | None:  # => None if a cycle makes ordering impossible
    in_degree: dict[str, int] = {  # => opens the initial all-zero in-degree map
        node: 0 for node in graph
    }  # => starts every node's in-degree at 0
    for node in graph:  # => O(V+E): counts how many edges point INTO each node
        for neighbor in graph[
            node  # => this node's own outgoing edges
        ]:  # => each outgoing edge increments the target's count
            in_degree[neighbor] += 1  # => one more prerequisite for neighbor

    queue: deque[str] = deque(  # => opens the initial ready-queue construction
        [node for node in graph if in_degree[node] == 0]  # => the zero-in-degree nodes
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
    "compile": ["link"],  # => must happen before "link"
    "link": ["test"],  # => must happen before "test"
    "fetch_deps": ["compile"],  # => the true starting point -- no prerequisites at all
    "test": [],  # => the terminal step -- nothing depends on it
}  # => closes the dependency map -- 4 build steps, one linear chain
order = kahn_topological_sort(graph)  # => a valid build order
print(order)  # => Output: ['fetch_deps', 'compile', 'link', 'test']

assert order is not None  # => confirms no cycle was detected
position = {  # => opens the node -> index lookup, built from the result order
    node: i  # => this node's position within the final order
    for i, node in enumerate(order)  # => pairs each node with its position
}  # => node -> its index in the order
assert position["fetch_deps"] < position["compile"]  # => a dependency comes first
assert position["compile"] < position["link"]  # => confirms edge direction is honored
assert position["link"] < position["test"]  # => confirms the last edge too
print("ex-35 OK")  # => Output: ex-35 OK
