"""Example 36: Topological Sort via DFS Finish-Time Ordering."""

# A DFS-based topological sort (co-18, co-17) is the mirror image of Kahn's
# algorithm: run DFS, and REVERSE the order nodes FINISH in. A node finishes
# only after every node reachable from it has already finished -- so it must
# come before all of them in a valid ordering.


def dfs_topological_sort(  # => reverse of DFS finish order -- the mirror of Kahn's
    graph: dict[str, list[str]],  # => adjacency map: node -> list of nodes it points to
) -> list[str]:  # => assumes a DAG -- no cycle check here (that's Example 37)
    visited: set[str] = set()  # => nodes already fully explored
    finish_order: list[  # => opens the type annotation split across lines
        str
    ] = []  # => nodes appended in the order they FINISH, not start

    def recurse(node: str) -> None:  # => a standard recursive DFS visit
        visited.add(node)  # => marks node as being explored
        for neighbor in graph.get(node, []):  # => visits every outgoing edge
            if neighbor not in visited:  # => only recurse into undiscovered nodes
                recurse(neighbor)  # => fully explores neighbor before returning
        finish_order.append(node)  # => node is appended ONLY after ALL its descendants

    for node in graph:  # => handles disconnected pieces too, not just one component
        if node not in visited:  # => starts a fresh DFS from any unvisited node
            recurse(node)  # => explores this whole component

    return list(reversed(finish_order))  # => REVERSING finish order gives topo order


graph: dict[str, list[str]] = {  # => the same build-dependency DAG as Example 35
    "compile": ["link"],  # => must happen before "link"
    "link": ["test"],  # => must happen before "test"
    "fetch_deps": ["compile"],  # => the true starting point -- no prerequisites at all
    "test": [],  # => the terminal step -- nothing depends on it
}  # => closes the dependency map -- same 4 build steps as Example 35
order = dfs_topological_sort(graph)  # => a valid build order, via DFS this time
print(order)  # => Output: ['fetch_deps', 'compile', 'link', 'test']

position = {node: i for i, node in enumerate(order)}  # => node -> its index in order
assert (  # => opens the first edge-direction check
    position["fetch_deps"] < position["compile"]  # => True iff "fetch_deps" comes first
)  # => confirms edge direction honored
assert position["compile"] < position["link"]  # => confirms another edge's direction
assert position["link"] < position["test"]  # => confirms the last edge too
assert len(order) == len(graph)  # => confirms every node appears exactly once
print("ex-36 OK")  # => Output: ex-36 OK
