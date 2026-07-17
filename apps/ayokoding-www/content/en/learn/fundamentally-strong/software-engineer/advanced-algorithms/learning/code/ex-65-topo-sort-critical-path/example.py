"""Example 65: Critical Path via DP over a Topological Order."""

# The critical path (longest path through a DAG) combines two ideas
# (co-18, co-24): process tasks in TOPOLOGICAL order (co-18) so every
# predecessor is already finalized, then DP: earliest_finish[task] =
# duration[task] + the LATEST of its predecessors' earliest_finish times.
from collections import deque


def topological_order(graph: dict[str, list[str]]) -> list[str]:  # => Kahn's algorithm
    in_degree: dict[str, int] = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    queue: deque[str] = deque([node for node in graph if in_degree[node] == 0])
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order  # => a valid topological order (assumes a DAG -- no cycle check here)


def critical_path_length(
    graph: dict[str, list[str]], durations: dict[str, int]
) -> tuple[int, dict[str, int]]:  # => (total project length, earliest_finish per task)
    order = topological_order(
        graph
    )  # => process every predecessor before its successors
    predecessors: dict[str, list[str]] = {
        node: [] for node in graph
    }  # => reverse the edges -- who must finish before each task
    for u in graph:
        for v in graph[u]:
            predecessors[v].append(u)  # => u is a predecessor of v

    earliest_finish: dict[
        str, int
    ] = {}  # => DP table: task -> earliest completion time
    for (
        task
    ) in order:  # => processes in topo order -- every predecessor is already known
        latest_predecessor_finish = max(
            (earliest_finish[p] for p in predecessors[task]), default=0
        )  # => 0 if this task has no predecessors -- it can start immediately
        earliest_finish[task] = (
            durations[task] + latest_predecessor_finish
        )  # => this task's own duration, stacked on top of its slowest predecessor

    total_length = max(earliest_finish.values())  # => the whole PROJECT'S critical path
    return (
        total_length,
        earliest_finish,
    )  # => project length and every task's finish time


graph: dict[str, list[str]] = {  # => a small hand-computable project schedule
    "design": ["build_a", "build_b"],
    "build_a": ["test"],
    "build_b": ["test"],
    "test": [],
}
durations: dict[str, int] = {  # => how long each task takes, in days
    "design": 3,
    "build_a": 5,
    "build_b": 2,
    "test": 4,
}
total_length, finish_times = critical_path_length(graph, durations)
print(total_length)  # => Output: 12
print(finish_times["test"])  # => Output: 12

assert (
    total_length == 12
)  # => design(3) -> build_a(5, the SLOWER branch) -> test(4) = 12
assert finish_times["design"] == 3  # => no predecessors -- finishes at its own duration
assert finish_times["build_b"] == 5  # => 3 (design) + 2 (build_b) = 5, NOT critical
assert finish_times["build_a"] == 8  # => 3 (design) + 5 (build_a) = 8, the SLOWER path
print("ex-65 OK")  # => Output: ex-65 OK
