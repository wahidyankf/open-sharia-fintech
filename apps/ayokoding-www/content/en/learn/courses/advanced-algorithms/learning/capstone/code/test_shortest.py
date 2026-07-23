"""pytest coverage for shortest.py -- Dijkstra's shortest paths."""

import pytest

from shortest import dijkstra


def test_dijkstra_finds_the_cheaper_of_two_routes() -> None:
    graph = {
        "start": [("mid", 1), ("end", 10)],
        "mid": [("start", 1), ("end", 1)],
        "end": [("mid", 1), ("start", 10)],
    }
    distances = dijkstra(graph, "start")
    assert (
        distances["end"] == 2
    )  # => via "mid" (1+1), cheaper than the direct edge (10)


def test_dijkstra_reports_an_unreachable_node_as_infinity_not_a_crash() -> None:
    graph = {"a": [("b", 1)], "b": [], "island": []}  # => "island" has no incoming edge
    distances = dijkstra(graph, "a")
    assert distances["island"] == float(
        "inf"
    )  # => reported, not raised and not omitted


def test_dijkstra_rejects_an_unknown_source_node() -> None:
    with pytest.raises(KeyError):
        dijkstra({"a": []}, "ghost")


def test_dijkstra_rejects_a_negative_edge_weight() -> None:
    with pytest.raises(ValueError):
        dijkstra({"a": [("b", -1)], "b": []}, "a")


def test_dijkstra_matches_the_road_network_used_by_the_workbench() -> None:
    road_network = {
        "DEPOT": [("L1", 2), ("L2", 5)],
        "L1": [("DEPOT", 2), ("L2", 1), ("L3", 4)],
        "L2": [("DEPOT", 5), ("L1", 1), ("L3", 2)],
        "L3": [("L1", 4), ("L2", 2)],
    }
    distances = dijkstra(road_network, "DEPOT")
    assert distances == {"DEPOT": 0.0, "L1": 2.0, "L2": 3.0, "L3": 5.0}
