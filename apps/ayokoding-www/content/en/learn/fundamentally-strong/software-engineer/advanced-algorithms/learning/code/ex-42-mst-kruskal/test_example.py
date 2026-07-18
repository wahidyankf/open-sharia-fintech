"""Example 42: pytest verification for Kruskal's MST."""

from example import kruskal_mst


def test_mst_has_exactly_n_minus_1_edges() -> None:
    n = 4
    edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10)]
    mst_edges, _ = kruskal_mst(n, edges)
    assert len(mst_edges) == n - 1


def test_mst_total_weight_matches_known_minimum() -> None:
    n = 5
    edges = [
        (0, 1, 2),
        (0, 3, 6),
        (1, 2, 3),
        (1, 3, 8),
        (1, 4, 5),
        (2, 4, 7),
        (3, 4, 9),
    ]
    _, total = kruskal_mst(n, edges)
    assert total == 16


# => Run: pytest -- Output: 2 passed
