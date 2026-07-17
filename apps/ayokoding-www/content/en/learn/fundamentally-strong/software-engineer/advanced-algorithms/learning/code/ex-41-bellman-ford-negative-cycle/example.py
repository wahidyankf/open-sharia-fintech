"""Example 41: Detect a Negative Cycle on Bellman-Ford's Nth Relaxation Round."""

# After V-1 relaxation rounds, distances are final -- UNLESS a negative cycle
# exists, in which case an Nth round can STILL improve some distance (co-20).
# That single extra round is the whole detection mechanism: if anything still
# relaxes, "shortest path" is not even well-defined -- you could loop forever.


def bellman_ford_with_cycle_check(  # => runs V-1 rounds, then ONE extra detection round
    n: int,
    edges: list[tuple[int, int, int]],
    start: int,  # => node count, edges, origin
) -> tuple[list[float], bool]:  # => (distances, has_negative_cycle)
    dist: list[float] = [float("inf")] * n  # => every node starts at infinity
    dist[start] = 0  # => the start node is 0 away from itself
    for _ in range(n - 1):  # => the normal V-1 relaxation rounds
        for u, v, w in edges:  # => relaxes every edge, every pass
            if dist[u] + w < dist[v]:  # => found a strictly cheaper way to reach v
                dist[v] = (  # => opens the distance-improvement assignment
                    dist[u] + w  # => the new, cheaper distance to v
                )  # => a genuine improvement, still within round V-1
    has_negative_cycle = False  # => assumes no negative cycle until proven otherwise
    for u, v, w in edges:  # => the EXTRA, Nth round -- pure detection, no more updates
        if dist[u] + w < dist[v]:  # => still improvable after V-1 rounds is IMPOSSIBLE
            has_negative_cycle = True  # => ...unless a negative cycle exists
            break  # => one detected violation is proof enough
    return dist, has_negative_cycle  # => distances are UNRELIABLE if the flag is True


n = 4  # => 4 nodes, labeled 0..3
edges_with_negative_cycle: list[tuple[int, int, int]] = [
    (0, 1, 1),  # => the only edge INTO the cycle -- reaches node 1 to start it off
    (1, 2, -1),  # => first leg of the cycle
    (2, 3, -1),  # => second leg of the cycle
    (3, 1, -1),  # => 1 -> 2 -> 3 -> 1 sums to -3: a genuine negative CYCLE
]  # => closes the edge list -- the 1->2->3->1 loop keeps getting cheaper forever
_, has_cycle = bellman_ford_with_cycle_check(
    n, edges_with_negative_cycle, start=0
)  # => discards the (unreliable) distances
print(has_cycle)  # => Output: True

edges_without_cycle: list[tuple[int, int, int]] = [
    (0, 1, 1),  # => same starting edge as before
    (1, 2, -1),  # => same negative edge as before
    (2, 3, -1),  # => same negative EDGES, but no cycle -- a simple path this time
]  # => closes the edge list -- node 3 has no outgoing edge, so nothing loops back
_, no_cycle = bellman_ford_with_cycle_check(
    n, edges_without_cycle, start=0
)  # => same discard pattern
print(no_cycle)  # => Output: False

assert has_cycle is True  # => confirms the genuine negative cycle is flagged
assert no_cycle is False  # => confirms negative EDGES alone don't trigger a false flag
print("ex-41 OK")  # => Output: ex-41 OK
