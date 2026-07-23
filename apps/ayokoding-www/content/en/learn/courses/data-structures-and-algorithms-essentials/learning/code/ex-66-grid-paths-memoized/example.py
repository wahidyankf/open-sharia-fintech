"""Example 66: Count Unique Grid Paths, via Memoization."""

from functools import lru_cache  # => imports the stdlib memoizing decorator (co-19)


# Counts paths from (0,0) to (rows-1, cols-1), moving only right or down.
# Without caching, this recurrence re-explores the SAME sub-grid from many
# different starting cells -- memoization collapses that overlap.
@lru_cache(maxsize=None)  # => the same stdlib memoization tool as Example 63
def count_paths(rows: int, cols: int) -> int:  # => a recursive, cached function
    if rows == 1 or cols == 1:  # => BASE CASE -- only one straight-line path exists
        return 1  # => a single-row or single-column grid has exactly one path
    return count_paths(rows - 1, cols) + count_paths(
        rows, cols - 1
    )  # => came from above OR left


result = count_paths(3, 3)  # => a 3x3 grid has exactly 6 distinct right/down paths
print(result)  # => Output: 6

assert result == 6  # => confirms the known path count for a 3x3 grid
assert count_paths(1, 5) == 1  # => confirms a single-row grid has exactly one path
print("ex-66 OK")  # => Output: ex-66 OK
