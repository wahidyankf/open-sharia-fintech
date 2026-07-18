"""pytest coverage for graph.py -- build_graph, bfs/dfs, and topological_sort edge cases."""

import pytest

from graph import (
    GraphCycleError,
    bfs_order,
    build_graph,
    dfs_order,
    reachable_nodes,
    topological_sort,
)


def test_build_graph_includes_isolated_nodes_with_no_edges() -> None:
    graph = build_graph(["a", "b", "c"], [("a", "b")])
    assert graph == {"a": ["b"], "b": [], "c": []}  # => "c" present despite zero edges


def test_build_graph_rejects_an_edge_to_an_unknown_node() -> None:
    with pytest.raises(KeyError):
        build_graph(["a"], [("a", "ghost")])


def test_topological_sort_on_an_empty_graph_returns_an_empty_order() -> None:
    assert topological_sort({}) == []  # => the empty-graph edge case


def test_topological_sort_respects_every_dependency_edge() -> None:
    graph = build_graph(
        ["a", "b", "c", "d"], [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    )
    order = topological_sort(graph)
    positions = {node: i for i, node in enumerate(order)}
    assert positions["a"] < positions["b"] < positions["d"]
    assert positions["a"] < positions["c"] < positions["d"]


def test_topological_sort_on_a_disconnected_graph_still_orders_every_node() -> None:
    # Two components with no edge between them at all: "b" depends on "a" and
    # "d" depends on "c", but the a/b pair and c/d pair are otherwise unrelated.
    graph = build_graph(["a", "b", "c", "d"], [("a", "b"), ("c", "d")])
    order = topological_sort(graph)
    assert set(order) == {"a", "b", "c", "d"}  # => every node present, none dropped
    positions = {node: i for i, node in enumerate(order)}
    assert positions["a"] < positions["b"]
    assert positions["c"] < positions["d"]


def test_topological_sort_rejects_a_cyclic_graph() -> None:
    graph = build_graph(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
    with pytest.raises(GraphCycleError):
        topological_sort(graph)


def test_topological_sort_cycle_error_names_the_stuck_nodes() -> None:
    graph = build_graph(["a", "b", "independent"], [("a", "b"), ("b", "a")])
    with pytest.raises(GraphCycleError) as excinfo:
        topological_sort(graph)
    assert "a" in str(excinfo.value)
    assert "b" in str(excinfo.value)
    assert "independent" not in str(excinfo.value)  # the healthy node is not implicated


def test_bfs_and_dfs_agree_on_reachability_but_may_differ_on_order() -> None:
    graph = build_graph(
        ["a", "b", "c", "d"], [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    )
    assert (
        set(bfs_order(graph, "a")) == set(dfs_order(graph, "a")) == {"a", "b", "c", "d"}
    )
    assert bfs_order(graph, "a")[0] == "a"  # => both traversals start at the root
    assert dfs_order(graph, "a")[0] == "a"


def test_reachable_nodes_excludes_a_disconnected_component() -> None:
    graph = build_graph(["a", "b", "c", "d"], [("a", "b"), ("c", "d")])
    assert reachable_nodes(graph, "a") == {
        "a",
        "b",
    }  # => "c" and "d" are a SEPARATE component
