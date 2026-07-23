"""Example 37: pytest verification for Backtracking N-Queens."""

from example import no_two_queens_attack, solve_n_queens


def test_eight_queens_solution_has_no_attacking_pair() -> None:
    solution = solve_n_queens(8)  # => same size as the module-level demo
    assert solution is not None  # => a solution must exist for n=8
    assert len(solution) == 8  # => one queen per row
    assert no_two_queens_attack(solution)  # => the independent checker must confirm safety


def test_four_queens_also_solves_safely() -> None:
    solution = solve_n_queens(4)  # => a smaller board, still solvable
    assert solution is not None
    assert no_two_queens_attack(solution)


# => Run: pytest -- Output: 2 passed
