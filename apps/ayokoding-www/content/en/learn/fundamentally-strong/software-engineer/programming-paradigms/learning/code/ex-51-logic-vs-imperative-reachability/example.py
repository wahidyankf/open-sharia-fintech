"""Example 51: Logic vs Imperative Reachability."""

from collections import deque  # => deque gives O(1) popleft(), the BFS queue's core operation

edges: dict[str, list[str]] = {  # => a directed graph, shared by both approaches below
    "a": ["b", "c"],  # => a points to b and c
    "b": ["d"],  # => b points to d
    "c": [],  # => c has no outgoing edges
    "d": ["a"],  # => a cycle back to "a" -- both approaches must handle this without looping forever
    "e": [],  # => an unreachable, isolated node
}  # => closes the shared graph declaration


def reachable_via_inference(start: str, edges: dict[str, list[str]]) -> set[str]:  # => LOGIC-flavored
    # => rule: reachable(X, Y) :- edge(X, Y).  reachable(X, Z) :- edge(X, Y), reachable(Y, Z).
    known: set[str] = set()  # => the set of facts inferred so far (a fixed-point computation)
    frontier = set(edges.get(start, []))  # => seed with everything directly reachable via one edge
    while frontier - known:  # => keep inferring new facts until nothing new can be derived (fixed point)
        newly_known = frontier - known  # => facts inferred in THIS round that weren't already known
        known |= newly_known  # => add them to the known set
        frontier = known | {y for x in newly_known for y in edges.get(x, [])}  # => derive one more hop
    return known  # => the full set of inferred "reachable" facts


def reachable_via_bfs(start: str, edges: dict[str, list[str]]) -> set[str]:  # => IMPERATIVE: explicit BFS
    visited: set[str] = set()  # => mutable set, built up by explicit traversal
    queue: deque[str] = deque(edges.get(start, []))  # => explicit FIFO work queue
    while queue:  # => explicit loop draining the queue
        node = queue.popleft()  # => explicit dequeue
        if node in visited:  # => explicit cycle guard
            continue  # => skip re-processing an already-visited node -- prevents the cycle from looping forever
        visited.add(node)  # => explicit mutation
        queue.extend(edges.get(node, []))  # => explicit enqueue of newly discovered neighbors
    return visited  # => the fully built set


inference_result = reachable_via_inference("a", edges)  # => run the logic-flavored version
bfs_result = reachable_via_bfs("a", edges)  # => run the imperative version

print(sorted(inference_result))  # => a -> b,c; b -> d; d -> a: the cycle makes "a" reachable from itself too
# => Output: ['a', 'b', 'c', 'd']
print(inference_result == bfs_result)  # => both must compute the identical reachable set
# => Output: True
