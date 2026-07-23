"""Example 62: pytest verification for Wait-For Graph Cycle Detection."""

from example import find_cycle


def test_two_node_cycle_is_detected() -> None:
    graph = {"a": ["b"], "b": ["a"]}
    cycle = find_cycle(graph)
    assert cycle is not None and cycle[0] == cycle[-1]


def test_acyclic_graph_returns_none() -> None:
    graph = {"a": ["b"], "b": []}
    assert find_cycle(graph) is None


def test_three_node_cycle_is_detected() -> None:
    graph = {"t1": ["t2"], "t2": ["t3"], "t3": ["t1"]}
    cycle = find_cycle(graph)
    assert cycle is not None and len(cycle) == 4


# => Run: pytest -- Output: 3 passed
