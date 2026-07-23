"""Capstone: algorithm workbench -- topo sort + critical-path DP + Dijkstra, end to end.

Threads `graph.py`'s graph model/BFS/DFS/topological sort, `critical_path.py`'s
DP, and `shortest.py`'s Dijkstra into one runnable pipeline over a sample
project: a task DAG (what order, and how early can each task start) plus a
road network (how long until each task's resources arrive) -- a schedule is
FEASIBLE only if every task's resources arrive before that task's DP-computed
earliest start time. The task/road numbers deliberately match Example 80's
preview, so a reader can cross-check this hardened, module-based version
against that single-file sketch.
"""

from __future__ import annotations

from critical_path import critical_path
from graph import Graph, build_graph, dfs_order, reachable_nodes, topological_sort
from shortest import WeightedGraph, dijkstra

TASK_NODES: list[str] = ["design", "build_a", "build_b", "test"]
TASK_EDGES: list[tuple[str, str]] = [
    ("design", "build_a"),
    ("design", "build_b"),
    ("build_a", "test"),
    ("build_b", "test"),
]
DURATIONS: dict[str, int] = {"design": 3, "build_a": 5, "build_b": 2, "test": 4}

# A small road network: a DEPOT plus three job sites, connected by weighted
# (travel-time) edges.
ROAD_NETWORK: WeightedGraph = {
    "DEPOT": [("L1", 2), ("L2", 5)],
    "L1": [("DEPOT", 2), ("L2", 1), ("L3", 4)],
    "L2": [("DEPOT", 5), ("L1", 1), ("L3", 2)],
    "L3": [("L1", 4), ("L2", 2)],
}
TASK_LOCATION: dict[str, str] = {  # => which site each task's resources must reach
    "design": "DEPOT",
    "build_a": "L2",
    "build_b": "L1",
    "test": "L2",
}


def run_workbench() -> tuple[list[str], int, dict[str, int], dict[str, float], bool]:
    """Build the task graph, verify connectivity, then run the full topo+DP+Dijkstra pipeline."""
    task_graph: Graph = build_graph(TASK_NODES, TASK_EDGES)  # => O(n + e)

    # BFS and DFS from the same root must agree on WHICH nodes are reachable,
    # even though they disagree on the visit ORDER -- this is the co-17 check
    # that would catch a silently-disconnected task before it ever reaches
    # the DP step below.
    bfs_reached = reachable_nodes(task_graph, "design")  # => O(n + e)
    dfs_reached = set(dfs_order(task_graph, "design"))  # => O(n + e)
    if bfs_reached != dfs_reached or bfs_reached != set(task_graph):
        raise RuntimeError(
            "task graph must be fully reachable from design -- found a disconnected task"
        )

    order = topological_sort(
        task_graph
    )  # => O(n + e); raises GraphCycleError on a cycle
    project_length, earliest_start, _earliest_finish = critical_path(
        task_graph, DURATIONS
    )  # => O(n + e)
    travel_time = dijkstra(ROAD_NETWORK, "DEPOT")  # => O((n + e) log n)

    feasible = all(  # => every task's resources must arrive before that task must start
        travel_time[TASK_LOCATION[task]] <= earliest_start[task] for task in task_graph
    )
    return order, project_length, earliest_start, travel_time, feasible


def main() -> None:
    """CLI entry point: run the workbench and print each stage's result."""
    order, project_length, earliest_start, travel_time, feasible = run_workbench()
    print("topological order:", " -> ".join(order))
    print("critical path length:", project_length)
    print("earliest start times:", earliest_start)
    print("travel times from DEPOT:", travel_time)
    print("schedule feasible:", feasible)


if (
    __name__ == "__main__"
):  # => only runs main() when invoked directly, not when imported
    main()
