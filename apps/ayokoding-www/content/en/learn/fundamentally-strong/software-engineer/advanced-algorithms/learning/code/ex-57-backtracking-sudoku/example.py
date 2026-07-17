"""Example 57: Solve Sudoku by Constraint Backtracking."""

# Backtracking (co-25) fills the FIRST empty cell with each candidate 1-9,
# checking the row/column/3x3-box constraints before committing -- an
# invalid candidate is pruned immediately, never explored further.

Board = list[list[int]]  # => a 9x9 grid; 0 marks an empty cell


def find_empty(board: Board) -> tuple[int, int] | None:  # => the first 0 cell, or None
    for r in range(9):  # => scans row by row
        for c in range(9):
            if board[r][c] == 0:  # => an unfilled cell
                return (r, c)  # => the next cell backtracking should try to fill
    return None  # => no empty cells remain -- the board is completely filled


def is_valid(board: Board, r: int, c: int, digit: int) -> bool:  # => the 3 Sudoku rules
    if digit in board[r]:  # => RULE 1: digit must not already be in this row
        return False
    if digit in [board[i][c] for i in range(9)]:  # => RULE 2: nor in this column
        return False
    box_r, box_c = 3 * (r // 3), 3 * (c // 3)  # => the top-left corner of this 3x3 box
    for i in range(box_r, box_r + 3):  # => RULE 3: nor anywhere in this 3x3 box
        for j in range(box_c, box_c + 3):
            if board[i][j] == digit:
                return False
    return True  # => digit violates none of the three rules at this position


def solve_sudoku(board: Board) -> bool:  # => mutates board in place; True if solved
    empty = find_empty(board)  # => finds the next cell needing a digit
    if empty is None:  # => base case: no empty cells left -- solved!
        return True
    r, c = empty  # => the (row, col) to try filling next
    for digit in range(1, 10):  # => tries every candidate digit 1-9
        if is_valid(
            board, r, c, digit
        ):  # => THE PRUNE: skip digits violating the rules
            board[r][c] = digit  # => commits this candidate
            if solve_sudoku(board):  # => recurses to fill the rest of the board
                return True  # => this whole branch led to a full solution
            board[r][c] = 0  # => BACKTRACK: this digit didn't lead anywhere -- undo it
    return False  # => no digit at (r, c) works -- an earlier choice must be wrong


puzzle: Board = [  # => a well-known easy Sudoku puzzle
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
solved = solve_sudoku(
    puzzle
)  # => mutates puzzle in place, returns whether it succeeded
print(solved)  # => Output: True

assert solved is True  # => confirms this puzzle was solvable
for r in range(9):  # => confirms every row is a permutation of 1-9
    assert sorted(puzzle[r]) == list(range(1, 10))
for c in range(9):  # => confirms every column is a permutation of 1-9
    assert sorted(puzzle[i][c] for i in range(9)) == list(range(1, 10))
for box_r in range(0, 9, 3):  # => confirms every 3x3 box is a permutation of 1-9
    for box_c in range(0, 9, 3):
        box_values = [puzzle[box_r + i][box_c + j] for i in range(3) for j in range(3)]
        assert sorted(box_values) == list(range(1, 10))
print("ex-57 OK")  # => Output: ex-57 OK
