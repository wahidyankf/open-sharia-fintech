"""Example 73: Detect a Cycle in a Directed Graph via DFS Coloring."""

# Three-color DFS: WHITE (unvisited), GRAY (on the current recursion path),
# BLACK (fully finished). A cycle exists iff DFS ever revisits a GRAY node (co-21, co-17).
WHITE, GRAY, BLACK = 0, 1, 2  # => the three states each node can be in


def has_cycle(graph: dict[str, list[str]]) -> bool:  # => outer driver over every node
    color: dict[str, int] = {
        node: WHITE for node in graph
    }  # => everyone starts unvisited

    def visit(node: str) -> bool:  # => a closure sharing the outer color dict
        color[node] = (
            GRAY  # => mark as "currently being explored" -- on the active path
        )
        for neighbor in graph[node]:  # => RECURSIVE CASE: check every outgoing edge
            if (
                color[neighbor] == GRAY
            ):  # => a back-edge to an ANCESTOR -- this IS a cycle
                return True  # => cycle found -- propagate immediately
            if color[neighbor] == WHITE and visit(
                neighbor
            ):  # => unvisited -- recurse into it
                return True  # => propagate a cycle found deeper in the recursion
        color[node] = BLACK  # => fully explored with no cycle through this node
        return False  # => no cycle found through this node's subtree

    return any(color[node] == WHITE and visit(node) for node in graph)
    # => tries every unvisited node as a DFS root -- the graph may be disconnected


cyclic_graph: dict[str, list[str]] = {
    "a": ["b"],
    "b": ["c"],
    "c": ["a"],
}  # => a->b->c->a
acyclic_graph: dict[str, list[str]] = {
    "a": ["b"],
    "b": ["c"],
    "c": [],
}  # => a->b->c, no way back

cyclic_result = has_cycle(cyclic_graph)  # => a->b->c->a revisits GRAY node "a"
acyclic_result = has_cycle(acyclic_graph)  # => a->b->c reaches BLACK with no revisits
print(cyclic_result)  # => Output: True
print(acyclic_result)  # => Output: False

assert cyclic_result is True  # => confirms the cyclic fixture is correctly flagged
assert acyclic_result is False  # => confirms the acyclic fixture is correctly cleared
print("ex-73 OK")  # => Output: ex-73 OK
