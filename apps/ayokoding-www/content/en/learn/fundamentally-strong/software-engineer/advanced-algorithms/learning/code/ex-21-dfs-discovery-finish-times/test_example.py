"""Example 21: pytest verification for DFS Discovery/Finish Times."""

from example import dfs_timestamps, intervals_are_nested_or_disjoint


def test_parenthesis_theorem_holds_on_a_diamond_graph() -> None:
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    disc, fin = dfs_timestamps(graph, "a")
    assert intervals_are_nested_or_disjoint(disc, fin)  # => never partially overlaps


def test_parenthesis_theorem_holds_on_a_star_graph() -> None:
    graph = {"center": ["a", "b", "c"], "a": [], "b": [], "c": []}
    disc, fin = dfs_timestamps(graph, "center")
    assert intervals_are_nested_or_disjoint(disc, fin)
    assert disc["center"] == 0  # => the star's center is always visited first


def test_every_node_gets_a_strictly_later_finish_than_discovery() -> None:
    graph = {"a": ["b"], "b": ["c"], "c": []}
    disc, fin = dfs_timestamps(graph, "a")
    for node in disc:
        assert fin[node] > disc[node]  # => a node always finishes after it starts


# => Run: pytest -- Output: 3 passed
