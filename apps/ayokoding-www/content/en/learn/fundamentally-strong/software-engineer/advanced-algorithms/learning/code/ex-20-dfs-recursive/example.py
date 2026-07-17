"""Example 20: Recursive DFS -- Collecting a Full Visit Order."""

# DFS (co-17) plunges as DEEP as possible before backtracking, using the call
# stack itself as its "frontier" -- the opposite exploration order from BFS's
# level-by-level queue, but both still visit every reachable node exactly once.


def dfs_visit_order(
    graph: dict[str, list[str]], start: str
) -> list[str]:  # => the order nodes are first visited
    visited: set[str] = set()  # => tracks nodes already seen, so none repeat
    order: list[str] = []  # => records the order this DFS actually visits nodes

    def recurse(node: str) -> None:  # => a closure sharing visited and order above
        visited.add(node)  # => marks node as seen BEFORE recursing into neighbors
        order.append(node)  # => records this visit
        for neighbor in graph.get(node, []):  # => tries every neighbor, in listed order
            if neighbor not in visited:  # => only recurse into genuinely new nodes
                recurse(neighbor)  # => plunges depth-first into this neighbor first

    recurse(start)  # => kicks off the recursion from the start node
    return order  # => every reachable node, in DFS visit order


graph: dict[str, list[str]] = {  # => the same graph shape as Example 19, for contrast
    "a": ["b", "c"],
    "b": ["a", "d"],
    "c": ["a", "d"],
    "d": ["b", "c", "e"],
    "e": ["d"],
}
order = dfs_visit_order(graph, "a")  # => DFS visit order, starting at "a"
print(order)  # => Output: ['a', 'b', 'd', 'c', 'e']

assert order[0] == "a"  # => the start node is always visited first
assert set(order) == {
    "a",
    "b",
    "c",
    "d",
    "e",
}  # => confirms every reachable node is visited exactly once
assert len(order) == len(set(order))  # => confirms no node is visited twice
print("ex-20 OK")  # => Output: ex-20 OK
