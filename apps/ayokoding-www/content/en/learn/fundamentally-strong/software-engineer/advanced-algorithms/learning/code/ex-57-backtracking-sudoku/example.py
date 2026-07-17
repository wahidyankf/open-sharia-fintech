"""Example 57: Solve Sudoku by Constraint Backtracking."""

# Backtracking (co-25) fills the FIRST empty cell with each candidate 1-9,
# checking the row/column/3x3-box constraints before committing -- an
# invalid candidate is pruned immediately, never explored further.

Board = list[list[int]]  # => a 9x9 grid; 0 marks an empty cell


def find_empty(board: Board) -> tuple[int, int] | None:  # => the first 0 cell, or None
    for r in range(9):  # => scans row by row
        for c in range(9):  # => and column by column within that row
            if board[r][c] == 0:  # => an unfilled cell
                return (r, c)  # => the next cell backtracking should try to fill
    return None  # => no empty cells remain -- the board is completely filled


def is_valid(board: Board, r: int, c: int, digit: int) -> bool:  # => the 3 Sudoku rules
    if digit in board[r]:  # => RULE 1: digit must not already be in this row
        return False  # => row conflict -- reject
    if digit in [board[i][c] for i in range(9)]:  # => RULE 2: nor in this column
        return False  # => column conflict -- reject
    box_r, box_c = 3 * (r // 3), 3 * (c // 3)  # => the top-left corner of this 3x3 box
    for i in range(box_r, box_r + 3):  # => RULE 3: nor anywhere in this 3x3 box
        for j in range(box_c, box_c + 3):  # => scans every cell of the 3x3 box
            if board[i][j] == digit:  # => the digit already appears in this box
                return False  # => box conflict -- reject
    return True  # => digit violates none of the three rules at this position


def solve_sudoku(board: Board) -> bool:  # => mutates board in place; True if solved
    empty = find_empty(board)  # => finds the next cell needing a digit
    if empty is None:  # => base case: no empty cells left -- solved!
        return True  # => nothing left to fill -- solved
    r, c = empty  # => the (row, col) to try filling next
    for digit in range(1, 10):  # => tries every candidate digit 1-9
        if is_valid(  # => opens the rule-check call
            board,  # => the current, partially-filled board
            r,  # => the row of the cell being tried
            c,  # => the column of the cell being tried
            digit,  # => the current board state and candidate digit
        ):  # => THE PRUNE: skip digits violating the rules
            board[r][c] = digit  # => commits this candidate
            if solve_sudoku(board):  # => recurses to fill the rest of the board
                return True  # => this whole branch led to a full solution
            board[r][c] = 0  # => BACKTRACK: this digit didn't lead anywhere -- undo it
    return False  # => no digit at (r, c) works -- an earlier choice must be wrong


puzzle: Board = [  # => a well-known easy Sudoku puzzle
    [5, 3, 0, 0, 7, 0, 0, 0, 0],  # => row 0
    [6, 0, 0, 1, 9, 5, 0, 0, 0],  # => row 1
    [0, 9, 8, 0, 0, 0, 0, 6, 0],  # => row 2
    [8, 0, 0, 0, 6, 0, 0, 0, 3],  # => row 3
    [4, 0, 0, 8, 0, 3, 0, 0, 1],  # => row 4
    [7, 0, 0, 0, 2, 0, 0, 0, 6],  # => row 5
    [0, 6, 0, 0, 0, 0, 2, 8, 0],  # => row 6
    [0, 0, 0, 4, 1, 9, 0, 0, 5],  # => row 7
    [0, 0, 0, 0, 8, 0, 0, 7, 9],  # => row 8
]  # => closes the puzzle literal -- 0 marks each empty cell
solved = solve_sudoku(  # => opens the solve call
    puzzle  # => mutated in place by the backtracking solver
)  # => mutates puzzle in place, returns whether it succeeded
print(solved)  # => Output: True

assert solved is True  # => confirms this puzzle was solvable
for r in range(9):  # => confirms every row is a permutation of 1-9
    assert sorted(puzzle[r]) == list(range(1, 10))  # => each row has every digit once
for c in range(9):  # => confirms every column is a permutation of 1-9
    assert sorted(  # => opens the column-values sort
        puzzle[i][c]  # => the value at row i, column c
        for i in range(9)  # => gathers column c's value from every row
    ) == list(range(1, 10))  # => each column has every digit once
for box_r in range(0, 9, 3):  # => confirms every 3x3 box is a permutation of 1-9
    for box_c in range(0, 9, 3):  # => scans every box's top-left corner
        box_values = [  # => opens the box-flattening comprehension
            puzzle[box_r + i][box_c + j]  # => the value at this box-relative cell
            for i in range(3)  # => 3 rows within the box
            for j in range(3)  # => one box's cells
        ]  # => flattens one 3x3 box into a flat list
        assert sorted(box_values) == list(
            range(1, 10)  # => the digits every box must contain exactly once
        )  # => each box has every digit once
print("ex-57 OK")  # => Output: ex-57 OK
