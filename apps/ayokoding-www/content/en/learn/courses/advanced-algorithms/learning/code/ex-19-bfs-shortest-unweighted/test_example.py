"""Example 19: pytest verification for BFS Shortest Hop-Count."""

from example import bfs_distances


def test_start_node_has_distance_zero() -> None:
    graph = {"a": ["b"], "b": ["a"]}
    assert bfs_distances(graph, "a")["a"] == 0


def test_distances_grow_by_exactly_one_per_hop_on_a_chain() -> None:
    graph = {"a": ["b"], "b": ["a", "c"], "c": ["b", "d"], "d": ["c"]}
    distances = bfs_distances(graph, "a")
    assert distances == {"a": 0, "b": 1, "c": 2, "d": 3}  # => a straight-line chain


def test_unreachable_node_is_simply_absent() -> None:
    graph = {"a": ["b"], "b": ["a"], "z": []}  # => z has no path from a
    distances = bfs_distances(graph, "a")
    assert "z" not in distances  # => unreachable nodes never get a distance entry


# => Run: pytest -- Output: 3 passed
