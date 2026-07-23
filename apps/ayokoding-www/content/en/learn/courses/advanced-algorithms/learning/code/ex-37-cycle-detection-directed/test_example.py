"""Example 37: pytest verification for Directed Cycle Detection."""

from example import has_cycle


def test_dag_reports_no_cycle() -> None:
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    assert has_cycle(graph) is False


def test_cyclic_graph_reports_a_cycle() -> None:
    graph = {"a": ["b"], "b": ["c"], "c": ["a"]}  # => a -> b -> c -> a
    assert has_cycle(graph) is True


def test_disconnected_dag_with_no_cycle_reports_false() -> None:
    graph = {"a": ["b"], "b": [], "x": ["y"], "y": []}
    assert has_cycle(graph) is False


# => Run: pytest -- Output: 3 passed
