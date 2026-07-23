"""Example 56: Grid Word Search via Backtracking."""

# Backtracking (co-25) tries extending a partial match in all 4 directions
# from each cell, marking cells VISITED so the same letter isn't reused
# twice in one path -- and un-marking them on the way back out, so other
# starting cells can still use that same grid position.


def word_search(grid: list[list[str]], word: str) -> bool:  # => True if word is found
    rows, cols = len(grid), len(grid[0])  # => the grid's dimensions
    visited: set[tuple[int, int]] = set()  # => cells used in the CURRENT path attempt

    def backtrack(r: int, c: int, index: int) -> bool:  # => tries to match word[index:]
        if index == len(word):  # => base case: every character has been matched
            return True  # => the whole word was found along this path
        if (  # => opens the four-way out-of-bounds/reuse/mismatch check
            r < 0  # => off the top edge
            or r >= rows  # => off the bottom edge
            or c < 0  # => off the left edge
            or c >= cols  # => off the right edge
            or (r, c) in visited  # => this cell is already used in the current path
            or grid[r][c] != word[index]  # => this cell's letter doesn't match
        ):  # => out of bounds, already used, or the letter doesn't match
            return False  # => THE PRUNE: this path cannot possibly succeed
        visited.add((r, c))  # => marks this cell as used for the current path
        found = (  # => opens the 4-direction exploration
            backtrack(r + 1, c, index + 1)  # => try DOWN
            or backtrack(r - 1, c, index + 1)  # => try UP
            or backtrack(r, c + 1, index + 1)  # => try RIGHT
            or backtrack(r, c - 1, index + 1)  # => try LEFT
        )  # => tries all 4 directions -- `or` short-circuits on the first success
        visited.remove(  # => opens the un-mark-cell call
            (r, c)  # => the cell to free
        )  # => BACKTRACK: frees this cell for OTHER starting attempts
        return found  # => whether any of the 4 directions led to a full match

    for r in range(rows):  # => tries every cell as a possible STARTING point
        for c in range(cols):  # => and every column within that row
            if backtrack(r, c, 0):  # => a full match was found starting here
                return True  # => no need to try any other starting cell
    return False  # => no starting cell led to a complete match anywhere


grid: list[list[str]] = [  # => a 3x4 letter grid
    ["A", "B", "C", "E"],  # => row 0
    ["S", "F", "C", "S"],  # => row 1
    ["A", "D", "E", "E"],  # => row 2
]  # => closes the grid literal
print(word_search(grid, "ABCCED"))  # => Output: True -- A->B->C->C->E->D, a valid path
print(word_search(grid, "SEE"))  # => Output: True -- S->E->E, a valid path
print(word_search(grid, "ABCB"))  # => Output: False -- would need to reuse a cell

assert word_search(grid, "ABCCED") is True  # => confirms a genuinely findable word
assert word_search(grid, "SEE") is True  # => confirms another findable word
assert word_search(grid, "ABCB") is False  # => confirms reuse is correctly disallowed
assert word_search(grid, "ZZZ") is False  # => confirms a wholly absent word fails too
print("ex-56 OK")  # => Output: ex-56 OK
