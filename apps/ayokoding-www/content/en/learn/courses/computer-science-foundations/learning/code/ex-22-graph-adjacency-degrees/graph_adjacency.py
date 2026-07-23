# learning/code/ex-22-graph-adjacency-degrees/graph_adjacency.py
"""Example 22: Adjacency List and Vertex Degrees."""  # => co-13: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from collections import defaultdict  # => co-13: builds the adjacency list without pre-declaring every vertex key

Edge = tuple[str, str]  # => co-13: an UNDIRECTED edge between two vertex labels


def build_adjacency(edges: list[Edge]) -> dict[str, list[str]]:  # => co-13: edge list -> adjacency-list view
    """Build an undirected adjacency list from a list of (u, v) edges."""  # => co-13: documents build_adjacency's contract -- no runtime output, just sets its __doc__
    adjacency: dict[str, list[str]] = defaultdict(list)  # => co-13: vertex -> list of its neighbors
    for u, v in edges:  # => co-13: each undirected edge adds BOTH directions to the adjacency list
        adjacency[u].append(v)  # => co-13: u is adjacent to v
        adjacency[v].append(u)  # => co-13: and, since the edge is undirected, v is adjacent to u too
    return dict(adjacency)  # => co-13: a plain dict -- easier for a reader to inspect than a defaultdict


def degree(adjacency: dict[str, list[str]], vertex: str) -> int:  # => co-13: the count of edges touching a vertex
    """The degree of a vertex: how many edges touch it."""  # => co-13: documents degree's contract -- no runtime output, just sets its __doc__
    return len(adjacency.get(vertex, []))  # => co-13: length of its neighbor list IS its degree, by construction


if __name__ == "__main__":  # => co-13: entry point -- this block runs only when the file executes directly, not on import
    edges: list[Edge] = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]  # => co-13: a small 4-vertex graph
    adjacency = build_adjacency(edges)  # => co-13: the adjacency-list representation of `edges`
    for vertex in sorted(adjacency):  # => co-13: one printed line per vertex, alphabetically for determinism
        print(f"{vertex}: neighbors={sorted(adjacency[vertex])} degree={degree(adjacency, vertex)}")  # => co-13
    expected_degrees = {"A": 2, "B": 2, "C": 3, "D": 1}  # => co-13: hand-counted from the edge list above
    for vertex, expected in expected_degrees.items():  # => co-13: cross-checks EVERY vertex against the hand count
        actual = degree(adjacency, vertex)  # => co-13: the adjacency-list-derived degree
        assert actual == expected, f"{vertex}'s degree must be {expected}, got {actual}"  # => co-13
    print(f"All degrees match the edge list: True")  # => co-13: reached only if every per-vertex assert passed
    # => co-13: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
