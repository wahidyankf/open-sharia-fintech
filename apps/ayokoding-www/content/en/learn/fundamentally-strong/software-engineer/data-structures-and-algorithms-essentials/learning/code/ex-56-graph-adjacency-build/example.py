"""Example 56: Build a Graph as a Dict-of-Lists Adjacency Map."""

# A dict-of-lists is the simplest general-purpose graph representation: each
# key is a node, each value is the list of its neighbors (co-21, co-08).
graph: dict[str, list[str]] = {  # => a 4-node, undirected-by-convention graph literal
    "a": ["b", "c"],  # => "a" connects to "b" and "c"
    "b": ["a", "d"],  # => "b" connects back to "a", plus "d"
    "c": ["a", "d"],  # => "c" connects back to "a", plus "d"
    "d": ["b", "c"],  # => "d" connects back to "b" and "c" -- a 4-node cycle
}  # => four keys total, each mapping to its own neighbor list

for (
    node,
    neighbors,
) in graph.items():  # => dict iteration is insertion-ordered (Python 3.7+)
    print(f"{node}: {neighbors}")  # => Output: one "node: [...]" line per graph key

assert graph["a"] == [
    "b",
    "c",
]  # => confirms a's neighbor list matches what was declared
assert "a" in graph["b"]  # => confirms the edge a-b is represented in BOTH directions
print("ex-56 OK")  # => Output: ex-56 OK
