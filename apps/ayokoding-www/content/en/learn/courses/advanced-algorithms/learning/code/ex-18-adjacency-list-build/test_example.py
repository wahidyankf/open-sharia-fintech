"""Example 18: pytest verification for Building an Adjacency List."""

from example import build_adjacency_list


def test_every_edge_is_represented_from_both_endpoints() -> None:
    graph = build_adjacency_list([("x", "y"), ("y", "z")])
    assert "y" in graph["x"]  # => x's neighbor list includes y
    assert "x" in graph["y"]  # => and y's neighbor list includes x, symmetrically
    assert "z" in graph["y"]  # => y also connects to z
    assert "y" in graph["z"]  # => and z connects back to y


def test_isolated_edge_list_produces_two_nodes() -> None:
    graph = build_adjacency_list([("p", "q")])
    assert set(graph.keys()) == {"p", "q"}  # => exactly the two endpoints, no more


# => Run: pytest -- Output: 2 passed
