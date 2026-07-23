"""Example 59: Least-Cost Path Through a Grid, via 2D DP."""

# dp[r][c] = cheapest cost to REACH (r, c), moving only right or down
# (co-24): it must have arrived from directly above or directly left,
# whichever was cheaper, plus this cell's own cost.


def min_cost_path(grid: list[list[int]]) -> int:  # => O(rows*cols) time and space
    rows, cols = len(grid), len(grid[0])  # => the grid's dimensions
    dp: list[list[int]] = [  # => opens the 2D table construction
        [0] * cols  # => one zero-filled row per grid row
        for _ in range(rows)  # => one fresh row of zeros per grid row
    ]  # => dp[r][c] = min cost to reach (r, c) from (0, 0)
    dp[0][0] = grid[0][0]  # => base case: reaching the start costs just its own cell
    for c in range(1, cols):  # => the FIRST row can only be reached by moving right
        dp[0][c] = (  # => opens the first-row assignment
            dp[0][c - 1] + grid[0][c]  # => running total plus this cell's own cost
        )  # => only one possible predecessor: the left
    for r in range(1, rows):  # => the FIRST column can only be reached by moving down
        dp[r][0] = dp[r - 1][0] + grid[r][0]  # => only one possible predecessor: above
    for r in range(1, rows):  # => fills the rest of the table, row by row
        for c in range(1, cols):  # => and column by column within each row
            dp[r][c] = grid[r][c] + min(  # => opens the cheaper-predecessor comparison
                dp[r - 1][c],  # => cost of arriving from directly above
                dp[r][c - 1],  # => cost via above vs cost via the left
            )  # => cheaper of "came from above" or "came from the left"
    return dp[rows - 1][  # => opens the final-cell lookup
        cols - 1  # => the destination's column index
    ]  # => the bottom-right cell: total cost of the best path


def min_cost_path_brute_force(grid: list[list[int]]) -> int:  # => O(2^(rows+cols))
    rows, cols = len(grid), len(grid[0])  # => the grid's dimensions

    def recurse(r: int, c: int) -> int:  # => explores EVERY right/down path, no memo
        if r == rows - 1 and c == cols - 1:  # => reached the destination
            return grid[r][c]  # => just this cell's own cost
        if r == rows - 1:  # => bottom row -- the ONLY option is moving right
            return grid[r][c] + recurse(
                r,  # => stays on the same, bottom row
                c + 1,  # => the only reachable neighbor from the bottom row
            )  # => this cell's cost plus moving right
        if c == cols - 1:  # => rightmost column -- the ONLY option is moving down
            return grid[r][c] + recurse(
                r + 1,  # => moves down a row
                c,  # => the only reachable neighbor from the rightmost column
            )  # => this cell's cost plus moving down
        return grid[r][c] + min(  # => opens the both-directions comparison
            recurse(r + 1, c),  # => cost of continuing downward
            recurse(r, c + 1),  # => cost via down vs cost via right
        )  # => tries BOTH directions, no reuse of overlapping subproblems

    return recurse(0, 0)  # => starts exploring from the top-left corner


grid: list[list[int]] = [  # => a small 3x3 cost grid
    [1, 3, 1],  # => row 0
    [1, 5, 1],  # => row 1
    [4, 2, 1],  # => row 2
]  # => closes the grid literal
fast_result = min_cost_path(grid)  # => O(rows*cols) DP answer
brute_result = min_cost_path_brute_force(grid)  # => exhaustive ground truth
print(fast_result)  # => Output: 7
print(brute_result)  # => Output: 7

assert fast_result == brute_result  # => confirms both approaches agree exactly
assert fast_result == 7  # => confirms the known-optimal path 1->3->1->1->1 sums to 7
print("ex-59 OK")  # => Output: ex-59 OK
