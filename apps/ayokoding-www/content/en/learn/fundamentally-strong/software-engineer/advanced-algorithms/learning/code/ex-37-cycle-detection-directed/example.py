"""Example 37: Detect a Cycle in a Directed Graph via DFS Coloring."""

# THREE colors (co-17, co-18), not just visited/unvisited, are what makes
# cycle detection possible: WHITE (unseen), GRAY (on the CURRENT recursion
# path), BLACK (fully finished). A back edge to a GRAY node means the current
# path loops back on itself -- exactly what a cycle is.
from enum import Enum, auto  # => Color is an Enum, not a bare string, for type safety


class Color(Enum):  # => three DFS visitation states -- enables cycle detection
    WHITE = auto()  # => not yet discovered
    GRAY = auto()  # => currently on the recursion stack -- an ANCESTOR of this call
    BLACK = auto()  # => fully explored, off the recursion stack


def has_cycle(  # => three-color DFS: a GRAY-to-GRAY edge means a back edge, i.e. a cycle
    graph: dict[str, list[str]],  # => adjacency map: node -> list of nodes it points to
) -> bool:  # => True iff a directed cycle exists
    color: dict[str, Color] = {  # => opens the dict-comprehension initializing colors
        node: Color.WHITE  # => every node begins undiscovered
        for node in graph  # => every node starts undiscovered
    }  # => all start WHITE

    def recurse(node: str) -> bool:  # => True if a cycle is found reachable from node
        color[node] = Color.GRAY  # => node is now an ANCESTOR on this recursion path
        for neighbor in graph.get(node, []):  # => tries every outgoing edge
            if color[neighbor] == Color.GRAY:  # => THE TELLTALE SIGN: an edge back to
                return True  # => an ancestor still on the stack -- a genuine cycle
            if color[
                neighbor  # => this neighbor's current visitation state
            ] == Color.WHITE and recurse(  # => only recurse into unseen nodes
                neighbor  # => the unvisited neighbor to explore next
            ):  # => explore unseen nodes
                return True  # => a cycle was found deeper in this branch
        color[node] = Color.BLACK  # => node is fully explored -- no longer an ancestor
        return False  # => no cycle found through this node

    return any(  # => True as soon as ANY unvisited component reports a cycle
        recurse(node)  # => explores each still-undiscovered component
        for node in graph
        if color[node] == Color.WHITE
    )  # => checks every component


acyclic_graph: dict[  # => opens the type annotation split across lines
    str, list[str]  # => same node/neighbor-list shape as every other graph example
] = {  # => a valid DAG -- Examples 35/36's build order
    "fetch_deps": ["compile"],  # => the true starting point -- no prerequisites at all
    "compile": ["link"],  # => must happen before "link"
    "link": ["test"],  # => must happen before "test"
    "test": [],  # => the terminal step -- nothing depends on it
}  # => closes the acyclic dependency map -- same DAG as Examples 35/36
cyclic_graph: dict[str, list[str]] = {  # => the SAME shape, but with one edge reversed
    "fetch_deps": ["compile"],  # => still the nominal starting point
    "compile": ["link"],  # => still points forward to "link"
    "link": ["test", "fetch_deps"],  # => "link" points back to "fetch_deps" -- a cycle
    "test": [],  # => still a terminal step, uninvolved in the cycle
}  # => closes the cyclic dependency map -- one back edge creates fetch_deps->compile->link->fetch_deps
print(has_cycle(acyclic_graph))  # => Output: False
print(has_cycle(cyclic_graph))  # => Output: True

assert (  # => opens the "acyclic graph correctly accepted" check
    has_cycle(acyclic_graph) is False  # => True only if no cycle was falsely detected
)  # => confirms a valid DAG is correctly accepted
assert has_cycle(cyclic_graph) is True  # => confirms the cycle is correctly detected
assert has_cycle({"a": ["a"]}) is True  # => a self-loop is the smallest possible cycle
print("ex-37 OK")  # => Output: ex-37 OK
