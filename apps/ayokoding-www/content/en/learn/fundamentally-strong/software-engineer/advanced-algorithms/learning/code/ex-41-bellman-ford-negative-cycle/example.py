"""Example 41: Detect a Negative Cycle on Bellman-Ford's Nth Relaxation Round."""

# After V-1 relaxation rounds, distances are final -- UNLESS a negative cycle
# exists, in which case an Nth round can STILL improve some distance (co-20).
# That single extra round is the whole detection mechanism: if anything still
# relaxes, "shortest path" is not even well-defined -- you could loop forever.


def bellman_ford_with_cycle_check(
    n: int, edges: list[tuple[int, int, int]], start: int
) -> tuple[list[float], bool]:  # => (distances, has_negative_cycle)
    dist: list[float] = [float("inf")] * n  # => every node starts at infinity
    dist[start] = 0  # => the start node is 0 away from itself
    for _ in range(n - 1):  # => the normal V-1 relaxation rounds
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = (
                    dist[u] + w
                )  # => a genuine improvement, still within round V-1
    has_negative_cycle = False  # => assumes no negative cycle until proven otherwise
    for u, v, w in edges:  # => the EXTRA, Nth round -- pure detection, no more updates
        if dist[u] + w < dist[v]:  # => still improvable after V-1 rounds is IMPOSSIBLE
            has_negative_cycle = True  # => ...unless a negative cycle exists
            break  # => one detected violation is proof enough
    return dist, has_negative_cycle  # => distances are UNRELIABLE if the flag is True


n = 4  # => 4 nodes, labeled 0..3
edges_with_negative_cycle: list[tuple[int, int, int]] = [
    (0, 1, 1),
    (1, 2, -1),
    (2, 3, -1),
    (3, 1, -1),  # => 1 -> 2 -> 3 -> 1 sums to -3: a genuine negative CYCLE
]
_, has_cycle = bellman_ford_with_cycle_check(n, edges_with_negative_cycle, start=0)
print(has_cycle)  # => Output: True

edges_without_cycle: list[tuple[int, int, int]] = [
    (0, 1, 1),
    (1, 2, -1),
    (2, 3, -1),  # => same negative EDGES, but no cycle -- a simple path this time
]
_, no_cycle = bellman_ford_with_cycle_check(n, edges_without_cycle, start=0)
print(no_cycle)  # => Output: False

assert has_cycle is True  # => confirms the genuine negative cycle is flagged
assert no_cycle is False  # => confirms negative EDGES alone don't trigger a false flag
print("ex-41 OK")  # => Output: ex-41 OK
