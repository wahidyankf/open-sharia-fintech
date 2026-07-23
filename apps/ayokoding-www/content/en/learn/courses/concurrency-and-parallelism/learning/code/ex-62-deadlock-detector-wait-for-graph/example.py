"""Example 62: Detecting a Deadlock -- Finding a Cycle in a Wait-For Graph."""

# => co-16, co-18: a "wait-for graph" has an edge A -> B whenever thread A is BLOCKED waiting for
# => something thread B currently holds; a deadlock exists IFF this graph contains a cycle


def find_cycle(wait_for: dict[str, list[str]]) -> list[str] | None:
    # => wait_for: e.g. {"A": ["B"], "B": ["A"]} means "A waits for B" AND "B waits for A"
    visiting: set[str] = set()  # => visiting: nodes on the CURRENT DFS path -- finding one again means a cycle
    visited: set[str] = set()  # => visited: nodes FULLY explored already -- never needs revisiting

    def dfs(node: str, path: list[str]) -> list[str] | None:
        if node in visiting:  # => we've seen `node` EARLIER on this SAME path -- that's the cycle
            cycle_start = path.index(node)  # => cycle_start: where `node` first appeared on this path
            return path[cycle_start:] + [node]  # => the cycle itself, e.g. ["A", "B", "A"]
        if node in visited:  # => already fully explored from a DIFFERENT starting point -- no cycle through here
            return None  # => nothing more to discover down this branch
        visiting.add(node)  # => marks `node` as "currently being explored" on THIS path
        for neighbor in wait_for.get(node, []):  # => follows every thread `node` is waiting for
            found = dfs(neighbor, path + [node])  # => recurses -- extends the path by this node
            if found is not None:  # => a cycle was found somewhere DOWNSTREAM of this call
                return found  # => propagates it straight back up to the original caller
        visiting.discard(node)  # => done exploring `node` on THIS path -- no cycle found through it
        visited.add(node)  # => marks `node` as fully explored, for good, across the whole graph
        return None  # => no cycle reachable from `node`

    for start_node in wait_for:  # => tries every node as a POTENTIAL cycle start, in case the graph is disconnected
        cycle = dfs(start_node, [])  # => searches for a cycle reachable from `start_node`
        if cycle is not None:  # => found one -- no need to check any other starting node
            return cycle  # => returns immediately with the first cycle discovered
    return None  # => no cycle exists anywhere in the graph -- no deadlock


if __name__ == "__main__":  # => module entry point
    deadlocked_graph = {"thread_a": ["thread_b"], "thread_b": ["thread_a"]}  # => ex-29's exact scenario: A waits for B, B waits for A
    cycle = find_cycle(deadlocked_graph)  # => cycle: the deadlock cycle, if any, found in this graph
    print(f"deadlocked_graph cycle={cycle}")  # => Output: deadlocked_graph cycle=['thread_a', 'thread_b', 'thread_a']

    ordered_graph = {"thread_a": ["thread_b"], "thread_b": []}  # => ex-30's fix: a GLOBAL order -- B never waits for A
    no_cycle = find_cycle(ordered_graph)  # => no_cycle: expected to be None -- this graph has no deadlock
    print(f"ordered_graph cycle={no_cycle}")  # => Output: ordered_graph cycle=None

    three_way_graph = {"t1": ["t2"], "t2": ["t3"], "t3": ["t1"]}  # => a LONGER cycle: t1 -> t2 -> t3 -> t1
    three_way_cycle = find_cycle(three_way_graph)  # => three_way_cycle: should also be detected, not just 2-node cycles
    print(f"three_way_graph cycle={three_way_cycle}")  # => Output: three_way_graph cycle=['t1', 't2', 't3', 't1']

    # => A depth-first search that tracks BOTH "currently on this path" (`visiting`) and "fully explored"
    # => (`visited`) can detect a cycle of ANY length in a wait-for graph in O(V+E) time -- re-encountering
    # => a node that's still `visiting` means the DFS has looped back on itself, which is EXACTLY what a
    # => deadlock is: thread A ultimately waiting, transitively, for something IT ALREADY holds (co-16).
    # => Production deadlock detectors (in databases, in the JVM) use this same wait-for-graph technique.
    assert cycle is not None and cycle[0] == cycle[-1]  # => confirms a genuine cycle was found and returned correctly
    assert no_cycle is None  # => confirms the lock-ordered graph is correctly recognized as deadlock-free
    assert three_way_cycle is not None and len(three_way_cycle) == 4  # => confirms a 3-node cycle is ALSO detected
    print("ex-62 OK")  # => Output: ex-62 OK
