"""Example 37: Detect a Cycle in a Directed Graph via DFS Coloring."""

# THREE colors (co-17, co-18), not just visited/unvisited, are what makes
# cycle detection possible: WHITE (unseen), GRAY (on the CURRENT recursion
# path), BLACK (fully finished). A back edge to a GRAY node means the current
# path loops back on itself -- exactly what a cycle is.
from enum import Enum, auto


class Color(Enum):
    WHITE = auto()  # => not yet discovered
    GRAY = auto()  # => currently on the recursion stack -- an ANCESTOR of this call
    BLACK = auto()  # => fully explored, off the recursion stack


def has_cycle(
    graph: dict[str, list[str]],
) -> bool:  # => True iff a directed cycle exists
    color: dict[str, Color] = {
        node: Color.WHITE for node in graph
    }  # => all start WHITE

    def recurse(node: str) -> bool:  # => True if a cycle is found reachable from node
        color[node] = Color.GRAY  # => node is now an ANCESTOR on this recursion path
        for neighbor in graph.get(node, []):  # => tries every outgoing edge
            if color[neighbor] == Color.GRAY:  # => THE TELLTALE SIGN: an edge back to
                return True  # => an ancestor still on the stack -- a genuine cycle
            if color[neighbor] == Color.WHITE and recurse(
                neighbor
            ):  # => explore unseen nodes
                return True  # => a cycle was found deeper in this branch
        color[node] = Color.BLACK  # => node is fully explored -- no longer an ancestor
        return False  # => no cycle found through this node

    return any(
        recurse(node) for node in graph if color[node] == Color.WHITE
    )  # => checks every component


acyclic_graph: dict[
    str, list[str]
] = {  # => a valid DAG -- Examples 35/36's build order
    "fetch_deps": ["compile"],
    "compile": ["link"],
    "link": ["test"],
    "test": [],
}
cyclic_graph: dict[str, list[str]] = {  # => the SAME shape, but with one edge reversed
    "fetch_deps": ["compile"],
    "compile": ["link"],
    "link": ["test", "fetch_deps"],  # => "link" points back to "fetch_deps" -- a cycle
    "test": [],
}
print(has_cycle(acyclic_graph))  # => Output: False
print(has_cycle(cyclic_graph))  # => Output: True

assert (
    has_cycle(acyclic_graph) is False
)  # => confirms a valid DAG is correctly accepted
assert has_cycle(cyclic_graph) is True  # => confirms the cycle is correctly detected
assert has_cycle({"a": ["a"]}) is True  # => a self-loop is the smallest possible cycle
print("ex-37 OK")  # => Output: ex-37 OK
