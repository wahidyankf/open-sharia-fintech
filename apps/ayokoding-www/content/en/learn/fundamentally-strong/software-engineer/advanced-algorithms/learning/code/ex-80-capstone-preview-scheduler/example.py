"""Example 80: Capstone Preview -- Topo-Sort + Critical-Path DP + Dijkstra, Threaded Together."""

# A realistic scheduler needs THREE algorithms at once (co-18, co-24, co-19):
# topological order (co-18) sequences dependent tasks; critical-path DP
# (co-24, building on Example 65) computes each task's earliest start/finish;
# Dijkstra (co-19, building on Example 63) computes travel time from a depot
# to each task's site. The schedule is FEASIBLE only if every task's
# required travel time fits before its DP-computed earliest start.
import heapq  # => Dijkstra's priority-queue frontier
from collections import deque  # => Kahn's topological-sort queue


def topological_order(graph: dict[str, list[str]]) -> list[str]:  # => Kahn's algorithm
    in_degree: dict[str, int] = {  # => opens the initial all-zero in-degree map
        node: 0  # => this node's predecessor count starts at zero
        for node in graph
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
            if in_degree[neighbor] == 0:  # => now has ALL its predecessors processed
                queue.append(neighbor)  # => neighbor is now safe to process too
    return order  # => a valid topological order (assumes a DAG -- no cycle check here)


def critical_path_schedule(  # => topo order + DP: computes every task's start/finish
    graph: dict[str, list[str]],  # => the task-dependency DAG
    durations: dict[str, int],  # => task graph + each task's duration
) -> tuple[
    int,  # => the total project length
    dict[str, int],  # => task -> earliest start time
    dict[str, int],  # => (project length, starts, finishes)
]:  # => (project length, starts, finishes)
    order = topological_order(  # => opens the topological-order call
        graph  # => the same task dependency graph
    )  # => process every predecessor before its successors
    predecessors: dict[str, list[str]] = {  # => opens the reversed-edge map
        node: []
        for node in graph  # => one empty predecessor list per task
    }  # => reverse the edges
    for u in graph:  # => scans every node's outgoing edges
        for v in graph[u]:  # => each edge u->v
            predecessors[v].append(u)  # => reverses the edges: who feeds into v
    earliest_start: dict[str, int] = {}  # => DP table: task -> earliest start time
    earliest_finish: dict[  # => opens the DP table's own type annotation
        str, int  # => task name -> earliest completion time
    ] = {}  # => DP table: task -> earliest completion time
    for task in order:  # => the DP pass, in topological order
        latest_pred_finish = max(  # => opens the slowest-predecessor lookup
            (  # => opens the predecessor-finish-times generator
                earliest_finish[p] for p in predecessors[task]
            ),  # => every predecessor's own finish time
            default=0,  # => 0 if no predecessors
        )  # => 0 if no predecessors -- this task can start immediately
        earliest_start[task] = (  # => opens the earliest-start assignment
            latest_pred_finish  # => can't start before ALL deps finish
        )
        earliest_finish[task] = (  # => opens the earliest-finish assignment
            durations[task] + latest_pred_finish  # => own duration plus the wait
        )  # => start plus own duration
    total_length = max(earliest_finish.values())  # => the whole project's critical path
    return (  # => opens the three-part result tuple
        total_length,  # => the overall project length
        earliest_start,  # => every task's own earliest-start time
        earliest_finish,
    )  # => length + every task's start/finish


def dijkstra_shortest_paths(  # => heap-driven shortest paths from a single source
    graph: dict[str, list[tuple[str, int]]],  # => node -> list of (neighbor, weight)
    start: str,  # => weighted adjacency list + source
) -> dict[str, float]:  # => shortest travel time from `start` to every reachable node
    distances: dict[str, float] = {  # => opens the initial all-infinity distance map
        node: float("inf")
        for node in graph  # => every node starts unreachable
    }  # => all unreached
    distances[start] = 0.0  # => the source reaches itself at cost 0
    heap: list[tuple[float, str]] = [  # => opens the initial single-entry heap
        (0.0, start)  # => the only known reachable node at distance 0
    ]  # => (distance, node), ordered by distance
    visited: set[str] = set()  # => nodes whose shortest distance is already finalized
    while heap:  # => keeps going until every reachable node is finalized
        dist, node = heapq.heappop(heap)  # => pops the CLOSEST unfinished node
        if (  # => opens the stale-entry check
            node in visited  # => True if this node's distance is already final
        ):  # => a stale heap entry -- already finalized via a shorter path
            continue  # => skip it, no work to redo
        visited.add(node)  # => this node's shortest distance is now final
        for neighbor, weight in graph[node]:  # => only relaxes THIS node's own edges
            new_dist = dist + weight  # => the candidate distance via this node
            if (  # => opens the strictly-shorter-path check
                new_dist < distances[neighbor]  # => True if this route just beat it
            ):  # => a strictly shorter path was just found
                distances[neighbor] = new_dist  # => records the improved distance
                heapq.heappush(  # => the heap may end up holding stale entries too
                    heap, (new_dist, neighbor)
                )  # => queues it for future expansion
    return distances  # => the final shortest distances from `start` to every node


# The SAME project from Example 65's critical-path demo.
task_graph: dict[str, list[str]] = {  # => opens the task dependency graph
    "design": ["build_a", "build_b"],  # => design must finish before either build
    "build_a": ["test"],  # => build_a must finish before test
    "build_b": ["test"],  # => build_b must finish before test
    "test": [],  # => the final task, with no successors
}  # => closes the task graph literal
durations: dict[str, int] = {  # => opens the per-task duration map
    "design": 3,  # => 3 days
    "build_a": 5,  # => 5 days -- the SLOWER of the two parallel builds
    "build_b": 2,  # => 2 days
    "test": 4,  # => 4 days
}  # => days per task
# => runs the topo-order + critical-path DP layer, built from Example 65's technique
total_length, earliest_start, earliest_finish = critical_path_schedule(
    task_graph,  # => the task-dependency DAG
    durations,  # => the same task graph and durations
)  # => runs the topo-order + critical-path DP layer

# A small road network: a DEPOT plus three job sites, connected by
# weighted (travel-time) edges -- structurally the same graph shape as
# Example 63's Dijkstra demo.
road_network: dict[str, list[tuple[str, int]]] = {  # => opens the road-network graph
    "DEPOT": [("L1", 2), ("L2", 5)],  # => depot connects directly to L1 and L2
    "L1": [("DEPOT", 2), ("L2", 1), ("L3", 4)],  # => L1's own direct connections
    "L2": [("DEPOT", 5), ("L1", 1), ("L3", 2)],  # => L2's own direct connections
    "L3": [("L1", 4), ("L2", 2)],  # => L3's own direct connections
}  # => closes the road-network literal
travel_time = dijkstra_shortest_paths(  # => opens the Dijkstra layer call
    road_network,  # => the weighted road-network adjacency map
    "DEPOT",  # => the road graph and the fixed starting depot
)  # => shortest time FROM depot

task_location: dict[str, str] = {  # => which site each task's resources must reach
    "design": "DEPOT",  # => design happens at the depot itself
    "build_a": "L2",  # => build_a's resources must reach L2
    "build_b": "L1",  # => build_b's resources must reach L1
    "test": "L2",  # => test's resources must reach L2
}  # => closes the task-location mapping

# => the end-to-end check: does every task's site get reached before its DP start time?
feasible = True  # => tracks whether EVERY task's resources arrive in time
for task in task_graph:  # => threads all three algorithms' outputs together
    required_travel = travel_time[task_location[task]]  # => from Dijkstra
    start_time = earliest_start[task]  # => from the critical-path DP
    if (  # => opens the feasibility comparison
        required_travel  # => how long resources take to reach this task's site
        > start_time  # => arrival happens strictly AFTER the required start
    ):  # => resources would arrive AFTER the task must start
        feasible = False  # => the end-to-end schedule is infeasible for this task

print(total_length)  # => Output: 12 -- the project's critical path, matching Example 65
print(earliest_start)  # => Output: {'design': 0, 'build_a': 3, 'build_b': 3, 'test': 8}
print(feasible)  # => Output: True -- every task's resources arrive in time

assert (  # => opens the known-critical-path-length check
    total_length == 12  # => the known critical-path length for this same project
)  # => confirms the DP layer still agrees with Example 65's answer
assert earliest_start == {  # => opens the exact-start-times comparison
    "design": 0,  # => no predecessors -- starts immediately
    "build_a": 3,  # => waits for design (3 days) to finish
    "build_b": 3,  # => also waits for design (3 days) to finish
    "test": 8,  # => waits for the SLOWER of build_a/build_b to finish
}  # => confirms the exact DP-computed start times
assert (  # => opens the known-shortest-distance check
    travel_time["L3"] == 5  # => the known shortest DEPOT -> L3 distance
)  # => confirms Dijkstra's shortest DEPOT -> L3 path (via L2)
assert (  # => opens the end-to-end feasibility check
    feasible  # => every task's travel time fit before its required start
)  # => confirms the END-TO-END schedule -- topo + DP + Dijkstra -- holds together
print("ex-80 OK")  # => Output: ex-80 OK
