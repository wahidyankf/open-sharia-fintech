"""Example 57: pytest verification for Sudoku Backtracking."""

from example import is_valid, solve_sudoku


def test_solves_a_known_easy_puzzle() -> None:
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    assert solve_sudoku(puzzle) is True
    assert puzzle[0] == [5, 3, 4, 6, 7, 8, 9, 1, 2]  # => the known solved first row


def test_is_valid_rejects_a_row_duplicate() -> None:
    board = [[0] * 9 for _ in range(9)]
    board[0][0] = 5
    assert is_valid(board, 0, 1, 5) is False  # => 5 already in row 0
    assert is_valid(board, 0, 1, 6) is True  # => 6 is not yet used anywhere relevant


# => Run: pytest -- Output: 2 passed
