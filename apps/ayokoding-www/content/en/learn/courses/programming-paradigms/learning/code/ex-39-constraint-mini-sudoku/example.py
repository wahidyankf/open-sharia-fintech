"""Example 39: Constraint Mini Sudoku (4x4)."""

Board = list[list[int]]  # => a 4x4 grid; 0 marks an empty cell

# => DECLARE the puzzle: 0 = empty, otherwise a fixed clue -- one valid 4x4 sudoku with three clues
puzzle: Board = [  # => four rows, four clues total -- the rest is left for the solver to fill in
    [1, 0, 0, 0],  # => row 0: a 1 fixed in column 0
    [0, 0, 1, 0],  # => row 1: a 1 fixed in column 2
    [0, 1, 0, 0],  # => row 2: a 1 fixed in column 1
    [0, 0, 0, 1],  # => row 3: a 1 fixed in column 3
]  # => closes the puzzle's initial 4x4 grid


def box_id(row: int, col: int) -> tuple[int, int]:  # => which 2x2 box a cell belongs to
    return (row // 2, col // 2)  # => integer division groups rows/cols into 2x2 quadrants


def is_valid(board: Board, row: int, col: int, value: int) -> bool:  # => the three sudoku constraints
    if any(board[row][c] == value for c in range(4)):  # => row constraint: no repeat in the row
        return False  # => reject immediately -- no need to check column or box constraints
    if any(board[r][col] == value for r in range(4)):  # => column constraint: no repeat in the column
        return False  # => reject immediately -- no need to check the box constraint
    br, bc = box_id(row, col)  # => box constraint: no repeat in the same 2x2 box
    for r in range(br * 2, br * 2 + 2):  # => the two rows of this cell's own 2x2 box
        for c in range(bc * 2, bc * 2 + 2):  # => the two columns of this cell's own 2x2 box
            if board[r][c] == value:  # => a same-box cell already holds this value
                return False  # => reject -- the value would appear twice in the same box
    return True  # => all three constraints satisfied


def solve(board: Board) -> Board | None:  # => backtracking search over empty cells
    for row in range(4):  # => find the first empty cell, in reading order
        for col in range(4):  # => scan every column of this row before moving to the next row
            if board[row][col] == 0:  # => this is the next cell to fill
                for value in range(1, 5):  # => CHOICE POINT: try every candidate digit 1-4
                    if is_valid(board, row, col, value):  # => only try digits that satisfy all constraints
                        board[row][col] = value  # => tentatively place it
                        if solve(board):  # => recurse into the rest of the board
                            return board  # => success propagates straight up -- no undo needed here
                        board[row][col] = 0  # => BACKTRACK: undo, try the next candidate digit
                return None  # => no digit worked for this cell given the current partial board
    return board  # => no empty cells remain -- fully solved


solution = solve([row[:] for row in puzzle])  # => solve a COPY so the original `puzzle` stays untouched
assert solution is not None  # => narrow away None -- this puzzle's three clues always admit a solution
print(solution)  # => a fully filled, constraint-satisfying 4x4 grid
# => Output: [[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]]
rows_ok = all(sorted(row) == [1, 2, 3, 4] for row in solution)  # => every row has 1-4 exactly once
cols_ok = all(sorted(solution[r][c] for r in range(4)) == [1, 2, 3, 4] for c in range(4))  # => every column
print(rows_ok and cols_ok)  # => independently confirms rows and columns are valid
# => Output: True
