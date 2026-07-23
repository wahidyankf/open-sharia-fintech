"""Example 18: Build a Graph as an Adjacency List from a Raw Edge List."""

# The adjacency-list representation (co-17) maps each node to the list of its
# neighbors -- O(1) to add an edge, O(degree) to enumerate a node's neighbors,
# and O(V+E) total space, versus an adjacency MATRIX's O(V^2) regardless of E.


def build_adjacency_list(  # => builds an UNDIRECTED graph -- each edge added both ways
    edges: list[tuple[str, str]],  # => flat list of (source, target) pairs
) -> dict[str, list[str]]:  # => converts a flat edge list into a neighbor map
    graph: dict[str, list[str]] = {}  # => starts with no nodes at all
    for u, v in edges:  # => walks each (source, target) edge pair once, O(E) total
        graph.setdefault(u, []).append(v)  # => records u -> v, creating u if new
        graph.setdefault(v, []).append(u)  # => records v -> u too -- UNDIRECTED graph
    return graph  # => a fully built node -> neighbor-list map


edge_list: list[tuple[str, str]] = [  # => opens the raw edge list -- 4 nodes, 4 edges
    ("a", "b"),  # => connects a and b
    ("a", "c"),  # => connects a and c -- a now has two neighbors
    ("b", "d"),  # => connects b and d
    ("c", "d"),  # => connects c and d -- closes the square (a-b-d-c-a)
]  # => a 4-node square graph
graph = build_adjacency_list(edge_list)  # => O(V+E): builds the full adjacency map
for node in sorted(graph):  # => sorted() just for deterministic print order
    print(f"{node}: {sorted(graph[node])}")  # => Output: one "node: [...]" per node

assert sorted(graph["a"]) == ["b", "c"]  # => confirms a's two neighbors
assert sorted(graph["d"]) == ["b", "c"]  # => confirms d's two neighbors
assert "a" in graph["b"]  # => confirms the edge a-b is represented from b's side too
assert len(graph) == 4  # => confirms exactly 4 distinct nodes were discovered
print("ex-18 OK")  # => Output: ex-18 OK
