"""Example 53: pytest verification for N-Queens Backtracking."""

from example import solve_n_queens


def test_known_solution_counts_for_small_n() -> None:
    assert solve_n_queens(1) == 1  # => trivially one way to place a single queen
    assert solve_n_queens(4) == 2
    assert solve_n_queens(8) == 92


def test_n_equals_two_and_three_have_no_solutions() -> None:
    assert solve_n_queens(2) == 0  # => too small a board to avoid all attacks
    assert solve_n_queens(3) == 0


# => Run: pytest -- Output: 2 passed
