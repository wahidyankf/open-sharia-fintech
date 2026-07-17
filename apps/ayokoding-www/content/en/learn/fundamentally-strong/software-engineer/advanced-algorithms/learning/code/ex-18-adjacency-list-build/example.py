"""Example 18: Build a Graph as an Adjacency List from a Raw Edge List."""

# The adjacency-list representation (co-17) maps each node to the list of its
# neighbors -- O(1) to add an edge, O(degree) to enumerate a node's neighbors,
# and O(V+E) total space, versus an adjacency MATRIX's O(V^2) regardless of E.


def build_adjacency_list(
    edges: list[tuple[str, str]],
) -> dict[str, list[str]]:  # => converts a flat edge list into a neighbor map
    graph: dict[str, list[str]] = {}  # => starts with no nodes at all
    for u, v in edges:  # => walks each (source, target) edge pair once, O(E) total
        graph.setdefault(u, []).append(v)  # => records u -> v, creating u if new
        graph.setdefault(v, []).append(u)  # => records v -> u too -- UNDIRECTED graph
    return graph  # => a fully built node -> neighbor-list map


edge_list: list[tuple[str, str]] = [
    ("a", "b"),
    ("a", "c"),
    ("b", "d"),
    ("c", "d"),
]  # => a 4-node square graph
graph = build_adjacency_list(edge_list)  # => O(V+E): builds the full adjacency map
for node in sorted(graph):  # => sorted() just for deterministic print order
    print(f"{node}: {sorted(graph[node])}")  # => Output: one "node: [...]" per node

assert sorted(graph["a"]) == ["b", "c"]  # => confirms a's two neighbors
assert sorted(graph["d"]) == ["b", "c"]  # => confirms d's two neighbors
assert "a" in graph["b"]  # => confirms the edge a-b is represented from b's side too
assert len(graph) == 4  # => confirms exactly 4 distinct nodes were discovered
print("ex-18 OK")  # => Output: ex-18 OK
