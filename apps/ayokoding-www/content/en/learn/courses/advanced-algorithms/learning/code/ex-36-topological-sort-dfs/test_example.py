"""Example 36: pytest verification for DFS-Based Topological Sort."""

from example import dfs_topological_sort


def test_every_edge_points_forward_in_the_resulting_order() -> None:
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    order = dfs_topological_sort(graph)
    position = {node: i for i, node in enumerate(order)}
    for u, neighbors in graph.items():
        for v in neighbors:
            assert position[u] < position[v]


def test_handles_a_disconnected_graph_with_two_components() -> None:
    graph = {"a": ["b"], "b": [], "x": ["y"], "y": []}
    order = dfs_topological_sort(graph)
    assert set(order) == {"a", "b", "x", "y"}  # => every node from both components


# => Run: pytest -- Output: 2 passed
