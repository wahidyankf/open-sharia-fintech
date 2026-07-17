"""Example 65: Critical Path via DP over a Topological Order."""

# The critical path (longest path through a DAG) combines two ideas
# (co-18, co-24): process tasks in TOPOLOGICAL order (co-18) so every
# predecessor is already finalized, then DP: earliest_finish[task] =
# duration[task] + the LATEST of its predecessors' earliest_finish times.
from collections import deque  # => O(1) popleft, unlike a plain list


def topological_order(graph: dict[str, list[str]]) -> list[str]:  # => Kahn's algorithm
    in_degree: dict[str, int] = {  # => opens the initial all-zero in-degree map
        node: 0  # => this node's predecessor count, before any edges are counted
        for node in graph  # => every node starts with zero known predecessors
    }  # => how many predecessors each node has
    for node in graph:  # => scans every node's outgoing edges
        for neighbor in graph[node]:  # => each edge node->neighbor
            in_degree[neighbor] += 1  # => neighbor gains one more predecessor
    queue: deque[str] = deque(  # => opens the initial ready-queue construction
        [node for node in graph if in_degree[node] == 0]  # => the zero-in-degree nodes
    )  # => sources first
    order: list[str] = []  # => accumulates the topological order as it's discovered
    while queue:  # => processes nodes in the order their in-degree hits zero
        node = queue.popleft()  # => the next node with all predecessors already emitted
        order.append(node)  # => records it as next in topological order
        for neighbor in graph[node]:  # => this node no longer blocks its successors
            in_degree[neighbor] -= 1  # => one fewer unresolved predecessor for neighbor
            if (  # => opens the last-predecessor check
                in_degree[neighbor] == 0  # => True once every predecessor has emitted
            ):  # => neighbor's LAST predecessor was just emitted
                queue.append(neighbor)  # => neighbor is now safe to process too
    return order  # => a valid topological order (assumes a DAG -- no cycle check here)


def critical_path_length(  # => DP over a topological order: the true project length
    graph: dict[str, list[str]],  # => the task-dependency DAG
    durations: dict[str, int],  # => task graph + each task's duration
) -> tuple[int, dict[str, int]]:  # => (total project length, earliest_finish per task)
    order = topological_order(  # => opens the topological-order call
        graph  # => the same task dependency graph
    )  # => process every predecessor before its successors
    predecessors: dict[  # => opens the reversed-edge map's type annotation
        str, list[str]  # => task name -> list of tasks that must finish first
    ] = {  # => opens the reversed-edge map construction
        node: []  # => this task starts with no known predecessors yet
        for node in graph  # => one empty predecessor list per task
    }  # => reverse the edges -- who must finish before each task
    for u in graph:  # => scans every node's outgoing edges
        for v in graph[u]:  # => each edge u->v
            predecessors[v].append(u)  # => u is a predecessor of v

    earliest_finish: dict[  # => opens the DP table's type annotation
        str, int  # => task name -> earliest completion time
    ] = {}  # => DP table: task -> earliest completion time
    for (  # => opens the topo-order iteration
        task  # => the current task, in topological order
    ) in order:  # => processes in topo order -- every predecessor is already known
        latest_predecessor_finish = max(  # => opens the slowest-predecessor lookup
            (  # => opens the predecessor-finish-times generator
                earliest_finish[p] for p in predecessors[task]
            ),  # => every predecessor's own finish time
            default=0,  # => 0 if no predecessors
        )  # => 0 if this task has no predecessors -- it can start immediately
        earliest_finish[task] = (  # => opens the DP-table assignment
            durations[task]  # => this task's own duration
            + latest_predecessor_finish  # => own duration plus the slowest wait
        )  # => this task's own duration, stacked on top of its slowest predecessor

    total_length = max(earliest_finish.values())  # => the whole PROJECT'S critical path
    return (  # => opens the result tuple
        total_length,  # => the overall project length
        earliest_finish,  # => every task's own earliest-finish time
    )  # => project length and every task's finish time


graph: dict[str, list[str]] = {  # => a small hand-computable project schedule
    "design": ["build_a", "build_b"],  # => design must finish before either build
    "build_a": ["test"],  # => build_a must finish before test
    "build_b": ["test"],  # => build_b must finish before test
    "test": [],  # => the final task, with no successors
}  # => closes the graph literal
durations: dict[str, int] = {  # => how long each task takes, in days
    "design": 3,  # => 3 days
    "build_a": 5,  # => 5 days -- the SLOWER of the two parallel builds
    "build_b": 2,  # => 2 days
    "test": 4,  # => 4 days
}  # => closes the durations literal
total_length, finish_times = critical_path_length(graph, durations)  # => runs the DP
print(total_length)  # => Output: 12
print(finish_times["test"])  # => Output: 12

assert (  # => opens the known-critical-path-length check
    total_length == 12  # => confirms the DP computed the known critical-path length
)  # => design(3) -> build_a(5, the SLOWER branch) -> test(4) = 12
assert finish_times["design"] == 3  # => no predecessors -- finishes at its own duration
assert finish_times["build_b"] == 5  # => 3 (design) + 2 (build_b) = 5, NOT critical
assert finish_times["build_a"] == 8  # => 3 (design) + 5 (build_a) = 8, the SLOWER path
print("ex-65 OK")  # => Output: ex-65 OK
