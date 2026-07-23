"""Example 20: pytest verification for Recursive DFS."""

from example import dfs_visit_order


def test_visits_every_reachable_node_exactly_once() -> None:
    graph = {"a": ["b", "c"], "b": ["a"], "c": ["a", "d"], "d": ["c"]}
    order = dfs_visit_order(graph, "a")
    assert sorted(order) == ["a", "b", "c", "d"]  # => all four nodes, no duplicates
    assert len(order) == len(set(order))  # => no repeats


def test_unreachable_node_is_excluded() -> None:
    graph = {"a": ["b"], "b": ["a"], "z": []}  # => z has no edge from a
    order = dfs_visit_order(graph, "a")
    assert "z" not in order  # => DFS from a never reaches the disconnected z


# => Run: pytest -- Output: 2 passed
