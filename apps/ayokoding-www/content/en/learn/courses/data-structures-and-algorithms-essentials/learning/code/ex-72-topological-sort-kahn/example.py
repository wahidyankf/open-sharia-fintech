"""Example 72: Topological Sort via Kahn's Algorithm."""

# Kahn's algorithm repeatedly removes nodes with in-degree 0 (no remaining
# prerequisites) -- a queue-driven generalization of BFS (co-21, co-05, co-08).
from collections import (
    deque,
)  # => imports the stdlib double-ended queue used as the frontier

graph: dict[
    str, list[str]
] = {  # => node -> list of nodes that DEPEND ON it (outgoing edges)
    "shirt": ["jacket"],  # => jacket depends on shirt going on first
    "socks": ["shoes"],  # => shoes depend on socks going on first
    "underwear": ["pants"],  # => pants depend on underwear going on first
    "pants": ["shoes", "jacket"],  # => shoes AND jacket both depend on pants
    "shoes": [],  # => nothing depends on shoes -- can be emitted last among its branch
    "jacket": [],  # => nothing depends on jacket -- can be emitted last among its branch
}  # => closes the dependency-graph literal


# Emits nodes only once every prerequisite has already been emitted (co-05, co-08).
def topological_sort(graph: dict[str, list[str]]) -> list[str]:  # => Kahn's algorithm
    in_degree: dict[str, int] = {
        node: 0 for node in graph
    }  # => counts unresolved prerequisites
    for node in graph:  # => outer pass over every node
        for dependent in graph[
            node
        ]:  # => inner pass over every OUTGOING edge from node
            in_degree[dependent] += (
                1  # => each edge adds ONE prerequisite to its target
            )

    queue: deque[str] = deque(node for node in graph if in_degree[node] == 0)
    # => seeds the queue with every node that has NO prerequisites at all
    order: list[str] = []  # => the resulting valid run order
    while queue:  # => O(V + E): every node and every edge is processed exactly once
        node = (
            queue.popleft()
        )  # => emit the next node with zero remaining prerequisites
        order.append(node)  # => records the emission
        for dependent in graph[node]:  # => relaxes every edge OUT of the emitted node
            in_degree[dependent] -= (
                1  # => one of dependent's prerequisites is now satisfied
            )
            if (
                in_degree[dependent] == 0
            ):  # => dependent has NO prerequisites left -- ready
                queue.append(dependent)  # => schedules dependent for emission
    return order  # => the full, dependency-respecting run order


order = topological_sort(graph)  # => a valid dressing order respecting every dependency
print(order)  # => Output: ['shirt', 'socks', 'underwear', 'pants', 'shoes', 'jacket']

assert len(order) == len(graph)  # => confirms every node was emitted exactly once
assert order.index("underwear") < order.index(
    "pants"
)  # => confirms deps precede dependents
assert order.index("pants") < order.index(
    "shoes"
)  # => confirms deps precede dependents
print("ex-72 OK")  # => Output: ex-72 OK
