"""Example 40: pytest verification for Bellman-Ford with Negative Edges."""

from example import bellman_ford


def test_matches_a_known_shortest_path_answer_with_negative_edges() -> None:
    n = 5
    edges = [
        (0, 1, 6),
        (0, 2, 7),
        (1, 2, 8),
        (1, 3, 5),
        (1, 4, -4),
        (2, 3, -3),
        (2, 4, 9),
        (3, 1, -2),
        (4, 3, 7),
        (4, 0, 2),
    ]
    distances = bellman_ford(n, edges, start=0)
    assert distances == [0, 2, 7, 4, -2]


def test_positive_only_graph_matches_a_simple_hand_computed_case() -> None:
    edges = [(0, 1, 1), (1, 2, 1), (0, 2, 5)]  # => 0->1->2 (2) beats direct 0->2 (5)
    distances = bellman_ford(3, edges, start=0)
    assert distances == [0, 1, 2]


# => Run: pytest -- Output: 2 passed
