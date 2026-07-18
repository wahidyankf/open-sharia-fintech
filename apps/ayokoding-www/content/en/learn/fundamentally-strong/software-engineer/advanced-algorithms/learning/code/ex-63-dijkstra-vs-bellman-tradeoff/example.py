"""Example 63: Dijkstra vs Bellman-Ford -- the Speed/Generality Trade, Measured."""

# On the SAME non-negative-weight graph, both algorithms agree on distances
# (co-19, co-20) -- but Dijkstra's heap-driven O((V+E) log V) does far fewer
# edge relaxations than Bellman-Ford's O(V*E) brute-force repetition.
# Bellman-Ford's payoff for that extra work is GENERALITY: it also handles
# negative edges, which would silently break Dijkstra's greedy assumption.
import heapq  # => the min-heap priority queue used to pick the closest unfinished node
import random  # => generates the random weighted graph both algorithms share


def dijkstra_counted(  # => heap-driven: only relaxes edges from the CLOSEST unfinished node
    graph: dict[int, list[tuple[int, int]]],  # => node -> list of (neighbor, weight)
    start: int,  # => adjacency list + source node
) -> tuple[dict[int, float], int]:  # => (distances, relaxation attempts)
    distances: dict[int, float] = {  # => opens the initial all-infinity distance map
        node: float("inf")  # => every node starts unreachable, by default
        for node in graph  # => every node starts unreachable
    }  # => all unreached
    distances[start] = 0  # => the source reaches itself at cost 0
    heap: list[tuple[float, int]] = [  # => opens the initial single-entry heap
        (0, start)  # => the only known reachable node at distance 0
    ]  # => (distance, node), ordered by distance
    visited: set[int] = set()  # => nodes whose shortest distance is already finalized
    relaxations = 0  # => counts every edge examined, across the whole run
    while heap:  # => keeps going until every reachable node is finalized
        dist, node = heapq.heappop(heap)  # => pops the CLOSEST unfinished node
        if (  # => opens the stale-entry check
            node in visited  # => True if this node's distance is already final
        ):  # => a stale heap entry -- already finalized via a shorter path
            continue  # => skip it, no work to redo
        visited.add(node)  # => this node's shortest distance is now final
        for neighbor, weight in graph[node]:  # => only relaxes THIS node's own edges
            relaxations += 1  # => one relaxation ATTEMPT per edge examined
            new_dist = dist + weight  # => the candidate distance via this node
            if (  # => opens the strictly-shorter-path check
                new_dist < distances[neighbor]  # => True if this route just beat it
            ):  # => a strictly shorter path was just found
                distances[neighbor] = new_dist  # => records the improved distance
                heapq.heappush(  # => the heap may end up holding stale entries too
                    heap,  # => the shared candidate-node priority queue
                    (new_dist, neighbor),  # => queues it for future expansion
                )  # => queues it for future expansion
    return distances, relaxations  # => the final shortest distances + total work done


def bellman_ford_counted(  # => brute-force: relaxes EVERY edge, EVERY round, no early exit
    n: int,  # => the number of nodes, labeled 0..n-1
    edges: list[tuple[int, int, int]],  # => (from, to, weight) triples
    start: int,  # => node count, edge list, source
) -> tuple[list[float], int]:  # => (distances, relaxation attempts)
    dist: list[float] = [float("inf")] * n  # => all nodes start unreached
    dist[start] = 0  # => the source reaches itself at cost 0
    relaxations = 0  # => counts every edge examined, across ALL n-1 rounds
    for _ in range(n - 1):  # => O(V) full rounds, EVEN once nothing more can improve
        for u, v, w in edges:  # => O(E) edges examined, every single round
            relaxations += 1  # => one relaxation attempt, whether or not it improves
            if (  # => opens the strictly-shorter-path check
                dist[u] + w < dist[v]  # => True if this edge just beat the known cost
            ):  # => a strictly shorter path via edge (u, v) was found
                dist[v] = dist[u] + w  # => records the improved distance
    return dist, relaxations  # => the final shortest distances + total work done


random.seed(91)  # => fixed seed -> reproducible graph structure
n = 40  # => 40 nodes, labeled 0..39
edge_list: list[tuple[int, int, int]] = [  # => a moderately dense random graph
    (u, v, random.randint(1, 20))  # => a random non-negative weight per candidate edge
    for u in range(n)  # => every possible source node
    for v in range(n)  # => every possible destination node
    if u != v  # => random weight
][:300]  # => 300 non-negative-weight edges

adjacency: dict[
    int, list[tuple[int, int]]  # => node -> list of (neighbor, weight)
] = {  # => opens the empty adjacency-map build
    i: []  # => this node starts with no outgoing edges yet
    for i in range(n)  # => every node starts with an empty edge list
}  # => empty adjacency lists
for u, v, w in edge_list:  # => builds Dijkstra's adjacency-list representation
    adjacency[u].append((v, w))  # => one directed edge per entry

dijkstra_distances, dijkstra_relaxations = dijkstra_counted(  # => opens the heap run
    adjacency,  # => the adjacency-list graph both algorithms will process
    0,  # => the same graph and source Bellman-Ford will also use
)  # => heap-driven run
bellman_distances, bellman_relaxations = bellman_ford_counted(  # => opens the brute run
    n,  # => the same node count as the graph above
    edge_list,  # => the same edges, in flat-list form for Bellman-Ford
    0,  # => the same graph and source Dijkstra already used
)  # => brute-force run

print(dijkstra_relaxations < bellman_relaxations)  # => Output: True
matches = all(  # => opens the pairwise distance-agreement check
    abs(dijkstra_distances[i] - bellman_distances[i])  # => this node's distance gap
    < 1e-9  # => allows for floating-point rounding only
    for i in range(n)  # => near-equal
)  # => both algorithms must AGREE, since edges here are all non-negative
print(matches)  # => Output: True

assert (  # => opens the Dijkstra-does-less-work check
    dijkstra_relaxations < bellman_relaxations  # => True only if Dijkstra truly won
)  # => confirms Dijkstra does meaningfully LESS work on this same graph
assert matches  # => confirms both agree exactly when weights are non-negative
print("ex-63 OK")  # => Output: ex-63 OK
