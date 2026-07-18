"""Example 34: pytest verification for Connected Components via Union-Find."""

from example import count_components


def test_disconnected_pairs_and_a_singleton() -> None:
    assert count_components(8, [(0, 1), (1, 2), (3, 4), (5, 6)]) == 4


def test_fully_connected_graph_has_one_component() -> None:
    edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
    assert count_components(5, edges) == 1


def test_no_edges_means_every_node_is_its_own_component() -> None:
    assert count_components(4, []) == 4


# => Run: pytest -- Output: 3 passed
