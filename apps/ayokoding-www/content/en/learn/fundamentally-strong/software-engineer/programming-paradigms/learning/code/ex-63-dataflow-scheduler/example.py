"""Example 63: Dataflow Scheduler (Parallel-Ready Batches)."""

Node = str  # => a type alias -- node names are just strings
graph: dict[Node, list[Node]] = {  # => node -> nodes it depends on (same shape as example 43)
    "d": ["b", "c"],  # => d depends on both b and c -- joins two branches
    "c": ["a"],  # => c depends only on a
    "b": ["a"],  # => b depends only on a
    "a": [],  # => a has no dependencies -- a source node
}  # => closes the dependency graph declaration


def schedule_batches(deps: dict[Node, list[Node]]) -> list[list[Node]]:  # => groups nodes into "waves"
    remaining = {n: set(d) for n, d in deps.items()}  # => a working copy of dependency sets, shrunk over time
    batches: list[list[Node]] = []  # => the final list of parallel-ready waves

    while remaining:  # => keep peeling off waves until every node is scheduled
        ready = sorted(n for n, deps_left in remaining.items() if not deps_left)  # => zero deps left = ready
        if not ready:  # => a cycle would leave every remaining node with an unmet dependency -- defensive check
            raise ValueError("cycle detected: no ready nodes")  # => fails loudly instead of looping forever
        batches.append(ready)  # => every node in `ready` can run IN PARALLEL -- none depends on another
        for node in ready:  # => remove this wave from the graph
            del remaining[node]  # => this node is fully scheduled -- no longer tracked as "remaining"
        for deps_left in remaining.values():  # => and remove it from every other node's remaining dependencies
            deps_left.difference_update(ready)  # => a node with an empty set becomes "ready" next iteration
    return batches  # => the full list of waves, in the order they must run


batches = schedule_batches(graph)  # => compute the parallel-ready waves
# => a scheduler could run every node inside one wave on a separate thread/process, safely
print(batches)  # => wave 1: a (no deps); wave 2: b, c (both depend only on a); wave 3: d (depends on b, c)
# => Output: [['a'], ['b', 'c'], ['d']]
