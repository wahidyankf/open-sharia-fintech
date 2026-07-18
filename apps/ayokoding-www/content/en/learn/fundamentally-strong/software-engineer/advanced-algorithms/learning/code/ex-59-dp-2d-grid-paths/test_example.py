"""Example 59: pytest verification for 2D DP Grid Paths."""

from example import min_cost_path, min_cost_path_brute_force


def test_matches_brute_force_enumeration_on_small_grids() -> None:
    grid = [[1, 2, 3], [4, 8, 2], [1, 5, 3]]
    assert min_cost_path(grid) == min_cost_path_brute_force(grid)


def test_single_row_grid_only_moves_right() -> None:
    grid = [[1, 2, 3, 4]]
    assert min_cost_path(grid) == 10  # => the only possible path


def test_single_cell_grid() -> None:
    assert min_cost_path([[5]]) == 5


# => Run: pytest -- Output: 3 passed
