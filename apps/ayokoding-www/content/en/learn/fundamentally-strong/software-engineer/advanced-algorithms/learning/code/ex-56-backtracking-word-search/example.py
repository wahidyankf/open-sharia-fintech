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
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or (r, c) in visited
            or grid[r][c] != word[index]
        ):  # => out of bounds, already used, or the letter doesn't match
            return False  # => THE PRUNE: this path cannot possibly succeed
        visited.add((r, c))  # => marks this cell as used for the current path
        found = (
            backtrack(r + 1, c, index + 1)
            or backtrack(r - 1, c, index + 1)
            or backtrack(r, c + 1, index + 1)
            or backtrack(r, c - 1, index + 1)
        )  # => tries all 4 directions -- `or` short-circuits on the first success
        visited.remove(
            (r, c)
        )  # => BACKTRACK: frees this cell for OTHER starting attempts
        return found  # => whether any of the 4 directions led to a full match

    for r in range(rows):  # => tries every cell as a possible STARTING point
        for c in range(cols):
            if backtrack(r, c, 0):  # => a full match was found starting here
                return True  # => no need to try any other starting cell
    return False  # => no starting cell led to a complete match anywhere


grid: list[list[str]] = [  # => a 3x4 letter grid
    ["A", "B", "C", "E"],
    ["S", "F", "C", "S"],
    ["A", "D", "E", "E"],
]
print(word_search(grid, "ABCCED"))  # => Output: True -- A->B->C->C->E->D, a valid path
print(word_search(grid, "SEE"))  # => Output: True -- S->E->E, a valid path
print(word_search(grid, "ABCB"))  # => Output: False -- would need to reuse a cell

assert word_search(grid, "ABCCED") is True  # => confirms a genuinely findable word
assert word_search(grid, "SEE") is True  # => confirms another findable word
assert word_search(grid, "ABCB") is False  # => confirms reuse is correctly disallowed
assert word_search(grid, "ZZZ") is False  # => confirms a wholly absent word fails too
print("ex-56 OK")  # => Output: ex-56 OK
