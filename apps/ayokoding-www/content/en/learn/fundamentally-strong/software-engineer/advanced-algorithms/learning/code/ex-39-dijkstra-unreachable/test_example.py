"""Example 39: pytest verification for Dijkstra on an Unreachable Node."""

import math

from example import dijkstra


def test_unreachable_node_reports_infinity_not_an_exception() -> None:
    graph = {"a": [("b", 1)], "b": [], "z": []}  # => z has no edge from a's component
    distances = dijkstra(graph, "a")
    assert math.isinf(distances["z"])  # => infinity, never a raised exception


def test_reachable_nodes_still_get_finite_distances() -> None:
    graph = {"a": [("b", 3)], "b": [], "z": []}
    distances = dijkstra(graph, "a")
    assert distances["b"] == 3
    assert not math.isinf(distances["b"])


# => Run: pytest -- Output: 2 passed
