"""Example 38: pytest verification for Dijkstra with a Heap."""

from example import dijkstra


def test_finds_shortest_path_through_an_indirect_route() -> None:
    graph = {
        "a": [("b", 4), ("c", 1)],
        "b": [("d", 1)],
        "c": [("b", 2), ("d", 5)],
        "d": [],
    }
    distances = dijkstra(graph, "a")
    assert distances["b"] == 3  # => indirect a->c->b beats the direct edge


def test_start_node_distance_is_zero() -> None:
    graph = {"x": [("y", 5)], "y": []}
    assert dijkstra(graph, "x")["x"] == 0


# => Run: pytest -- Output: 2 passed
