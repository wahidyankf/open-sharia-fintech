"""Example 64: pytest verification for A* Search."""

from example import a_star_grid, dijkstra_grid


def test_a_star_matches_dijkstra_cost_but_expands_fewer_nodes() -> None:
    rows, cols = 30, 30
    start, goal = (10, 10), (13, 12)
    d_cost, d_expanded = dijkstra_grid(rows, cols, start, goal)
    a_cost, a_expanded = a_star_grid(rows, cols, start, goal)
    assert d_cost == a_cost  # => same optimal cost
    assert a_expanded < d_expanded  # => A* explores meaningfully less


def test_adjacent_start_and_goal_cost_one() -> None:
    d_cost, _ = dijkstra_grid(5, 5, (0, 0), (0, 1))
    a_cost, _ = a_star_grid(5, 5, (0, 0), (0, 1))
    assert d_cost == a_cost == 1


# => Run: pytest -- Output: 2 passed
