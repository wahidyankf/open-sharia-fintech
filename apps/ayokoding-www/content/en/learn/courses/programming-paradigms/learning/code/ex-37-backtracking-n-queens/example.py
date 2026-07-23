"""Example 37: Backtracking N-Queens."""


def solve_n_queens(n: int) -> list[int] | None:  # => returns one solution: cols[row] = column of the queen
    cols: list[int] = []  # => the partial (and eventually full) placement, one column index per row

    def is_safe(row: int, col: int) -> bool:  # => can a queen go at (row, col) given queens placed so far?
        for placed_row, placed_col in enumerate(cols):  # => check against every already-placed queen
            if placed_col == col:  # => same column: an attack
                return False  # => reject immediately -- no need to check any other placed queen
            if abs(placed_col - col) == abs(placed_row - row):  # => same diagonal: an attack
                return False  # => reject immediately, same reasoning
        return True  # => no earlier queen attacks this square

    def backtrack(row: int) -> bool:  # => try to place a queen in every row, from `row` downward
        if row == n:  # => base case: every row has a queen -- a full solution was found
            return True  # => success propagates straight back up the recursion, no cols.pop() needed
        for col in range(n):  # => CHOICE POINT: try every column in this row
            if is_safe(row, col):  # => only attempt columns that don't conflict yet
                cols.append(col)  # => tentatively place the queen
                if backtrack(row + 1):  # => recurse to the next row
                    return True  # => the whole rest of the board solved -- propagate success up
                cols.pop()  # => BACKTRACK: that column led nowhere, undo it and try the next column
        return False  # => no column in this row works given the current partial placement

    return cols if backtrack(0) else None  # => cols is fully built only if backtrack(0) succeeded


def no_two_queens_attack(cols: list[int]) -> bool:  # => independent checker, used only for verification
    for r1 in range(len(cols)):  # => compare every pair of placed queens
        for r2 in range(r1 + 1, len(cols)):  # => r2 > r1 -- each pair checked exactly once, not twice
            if cols[r1] == cols[r2]:  # => same column
                return False  # => a violation was found -- no need to check any remaining pairs
            if abs(cols[r1] - cols[r2]) == abs(r1 - r2):  # => same diagonal
                return False  # => a violation was found -- no need to check any remaining pairs
    return True  # => every pair is safe


solution = solve_n_queens(8)  # => the classic 8-queens problem
assert solution is not None  # => narrow away None -- 8-queens always has a solution, matching test_example.py
print(solution)  # => one valid arrangement (the specific columns depend on search order, but it is safe)
# => Output: [0, 4, 7, 5, 2, 6, 1, 3]
print(no_two_queens_attack(solution))  # => independently confirms no two queens attack each other
# => Output: True
