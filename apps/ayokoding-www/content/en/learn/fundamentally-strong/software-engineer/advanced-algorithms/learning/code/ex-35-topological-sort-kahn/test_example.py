"""Example 35: pytest verification for Kahn's Topological Sort."""

from example import kahn_topological_sort


def test_every_edge_points_forward_in_the_resulting_order() -> None:
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    order = kahn_topological_sort(graph)
    assert order is not None
    position = {node: i for i, node in enumerate(order)}
    for u, neighbors in graph.items():
        for v in neighbors:
            assert position[u] < position[v]  # => u always precedes v


def test_a_valid_dag_produces_a_full_length_order() -> None:
    graph = {"x": ["y"], "y": ["z"], "z": []}
    order = kahn_topological_sort(graph)
    assert order is not None
    assert len(order) == 3


# => Run: pytest -- Output: 2 passed
