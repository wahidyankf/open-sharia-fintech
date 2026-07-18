"""pytest coverage for critical_path.py -- the DP over graph.py's topological order."""

import pytest

from critical_path import critical_path
from graph import GraphCycleError, build_graph


def test_critical_path_on_an_empty_graph_returns_zero() -> None:
    assert critical_path({}, {}) == (0, {}, {})  # => the empty-graph edge case


def test_critical_path_matches_a_hand_computed_diamond_dag() -> None:
    graph = build_graph(
        ["design", "build_a", "build_b", "test"],
        [
            ("design", "build_a"),
            ("design", "build_b"),
            ("build_a", "test"),
            ("build_b", "test"),
        ],
    )
    durations = {"design": 3, "build_a": 5, "build_b": 2, "test": 4}
    length, starts, finishes = critical_path(graph, durations)
    assert (
        length == 12
    )  # => the LONGER build_a branch (3+5=8) dominates build_b's (3+2=5)
    assert starts == {"design": 0, "build_a": 3, "build_b": 3, "test": 8}
    assert finishes == {"design": 3, "build_a": 8, "build_b": 5, "test": 12}


def test_critical_path_on_a_single_chain_is_a_pure_sum_of_durations() -> None:
    graph = build_graph(["a", "b", "c"], [("a", "b"), ("b", "c")])
    length, starts, _finishes = critical_path(graph, {"a": 2, "b": 3, "c": 1})
    assert length == 6  # => a single chain: 2 + 3 + 1
    assert starts == {"a": 0, "b": 2, "c": 5}


def test_critical_path_propagates_the_cycle_error_from_topological_sort() -> None:
    graph = build_graph(["a", "b"], [("a", "b"), ("b", "a")])
    with pytest.raises(GraphCycleError):
        critical_path(graph, {"a": 1, "b": 1})
