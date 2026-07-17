"""Example 80: Capstone Preview -- Topo-Sort + Critical-Path DP + Dijkstra, Threaded Together."""

# A realistic scheduler needs THREE algorithms at once (co-18, co-24, co-19):
# topological order (co-18) sequences dependent tasks; critical-path DP
# (co-24, building on Example 65) computes each task's earliest start/finish;
# Dijkstra (co-19, building on Example 63) computes travel time from a depot
# to each task's site. The schedule is FEASIBLE only if every task's
# required travel time fits before its DP-computed earliest start.
import heapq
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
            if in_degree[neighbor] == 0:  # => now has ALL its predecessors processed
                queue.append(neighbor)
    return order


def critical_path_schedule(
    graph: dict[str, list[str]], durations: dict[str, int]
) -> tuple[
    int, dict[str, int], dict[str, int]
]:  # => (project length, starts, finishes)
    order = topological_order(
        graph
    )  # => process every predecessor before its successors
    predecessors: dict[str, list[str]] = {node: [] for node in graph}
    for u in graph:
        for v in graph[u]:
            predecessors[v].append(u)  # => reverses the edges: who feeds into v
    earliest_start: dict[str, int] = {}
    earliest_finish: dict[str, int] = {}
    for task in order:  # => the DP pass, in topological order
        latest_pred_finish = max(
            (earliest_finish[p] for p in predecessors[task]), default=0
        )  # => 0 if no predecessors -- this task can start immediately
        earliest_start[task] = (
            latest_pred_finish  # => can't start before ALL deps finish
        )
        earliest_finish[task] = durations[task] + latest_pred_finish
    total_length = max(earliest_finish.values())  # => the whole project's critical path
    return total_length, earliest_start, earliest_finish


def dijkstra_shortest_paths(
    graph: dict[str, list[tuple[str, int]]], start: str
) -> dict[str, float]:  # => shortest travel time from `start` to every reachable node
    distances: dict[str, float] = {node: float("inf") for node in graph}
    distances[start] = 0.0
    heap: list[tuple[float, str]] = [(0.0, start)]
    visited: set[str] = set()
    while heap:
        dist, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    return distances


# The SAME project from Example 65's critical-path demo.
task_graph: dict[str, list[str]] = {
    "design": ["build_a", "build_b"],
    "build_a": ["test"],
    "build_b": ["test"],
    "test": [],
}
durations: dict[str, int] = {"design": 3, "build_a": 5, "build_b": 2, "test": 4}
total_length, earliest_start, earliest_finish = critical_path_schedule(
    task_graph, durations
)

# A small road network: a DEPOT plus three job sites, connected by
# weighted (travel-time) edges -- structurally the same graph shape as
# Example 63's Dijkstra demo.
road_network: dict[str, list[tuple[str, int]]] = {
    "DEPOT": [("L1", 2), ("L2", 5)],
    "L1": [("DEPOT", 2), ("L2", 1), ("L3", 4)],
    "L2": [("DEPOT", 5), ("L1", 1), ("L3", 2)],
    "L3": [("L1", 4), ("L2", 2)],
}
travel_time = dijkstra_shortest_paths(
    road_network, "DEPOT"
)  # => shortest time FROM depot

task_location: dict[str, str] = {  # => which site each task's resources must reach
    "design": "DEPOT",
    "build_a": "L2",
    "build_b": "L1",
    "test": "L2",
}

feasible = True  # => tracks whether EVERY task's resources arrive in time
for task in task_graph:  # => threads all three algorithms' outputs together
    required_travel = travel_time[task_location[task]]  # => from Dijkstra
    start_time = earliest_start[task]  # => from the critical-path DP
    if (
        required_travel > start_time
    ):  # => resources would arrive AFTER the task must start
        feasible = False

print(total_length)  # => Output: 12 -- the project's critical path, matching Example 65
print(earliest_start)  # => Output: {'design': 0, 'build_a': 3, 'build_b': 3, 'test': 8}
print(feasible)  # => Output: True -- every task's resources arrive in time

assert (
    total_length == 12
)  # => confirms the DP layer still agrees with Example 65's answer
assert earliest_start == {
    "design": 0,
    "build_a": 3,
    "build_b": 3,
    "test": 8,
}  # => confirms the exact DP-computed start times
assert (
    travel_time["L3"] == 5
)  # => confirms Dijkstra's shortest DEPOT -> L3 path (via L2)
assert (
    feasible
)  # => confirms the END-TO-END schedule -- topo + DP + Dijkstra -- holds together
print("ex-80 OK")  # => Output: ex-80 OK
