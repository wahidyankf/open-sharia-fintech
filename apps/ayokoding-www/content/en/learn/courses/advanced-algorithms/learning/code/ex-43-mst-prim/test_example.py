"""Example 43: pytest verification for Prim's MST."""

from example import prim_mst


def test_mst_total_weight_matches_kruskal_on_the_same_graph() -> None:
    adjacency = {
        0: [(1, 2), (3, 6)],
        1: [(0, 2), (2, 3), (3, 8), (4, 5)],
        2: [(1, 3), (4, 7)],
        3: [(0, 6), (1, 8), (4, 9)],
        4: [(1, 5), (2, 7), (3, 9)],
    }
    _, total = prim_mst(5, adjacency)
    assert total == 16  # => the same minimum weight Example 42's Kruskal found


def test_mst_has_exactly_n_minus_1_edges() -> None:
    adjacency = {0: [(1, 1), (2, 4)], 1: [(0, 1), (2, 2)], 2: [(0, 4), (1, 2)]}
    mst_edges, _ = prim_mst(3, adjacency)
    assert len(mst_edges) == 2


# => Run: pytest -- Output: 2 passed
