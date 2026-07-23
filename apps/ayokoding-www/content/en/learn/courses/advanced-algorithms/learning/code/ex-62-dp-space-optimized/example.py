"""Example 62: Space-Optimized 0/1 Knapsack -- O(capacity) Instead of O(n * capacity)."""

# Each row of the knapsack's 2D table only ever reads the PREVIOUS row
# (co-24, co-05) -- so a single 1D array can replace the whole table, IF
# updated capacity DECREASING for each item. Iterating backward guarantees
# each cell still reads last item's value (not this item's, reused twice).


def knapsack_2d_full_table(  # => the full O(n*capacity) table, kept only for comparison
    weights: list[int],  # => each item's own weight
    values: list[int],  # => each item's own value
    capacity: int,  # => item weights/values + limit
) -> int:  # => O(n * capacity) TIME and SPACE -- the full table, for comparison
    n = len(weights)  # => number of available items
    dp: list[list[int]] = [
        [0] * (capacity + 1)  # => one zero-filled row per item count
        for _ in range(n + 1)
    ]  # => full 2D table
    for i in range(1, n + 1):  # => considers items one at a time
        w, v = weights[i - 1], values[i - 1]  # => this item's own weight/value
        for c in range(capacity + 1):  # => every possible capacity, from 0 up
            dp[i][c] = dp[i - 1][c]  # => the SKIP option: value stays whatever it was
            if w <= c:  # => the TAKE option is only possible if it actually fits
                dp[i][c] = max(
                    dp[i][c],  # => the SKIP option's value
                    v + dp[i - 1][c - w],  # => the TAKE option's value
                )  # => best of skip vs take
    return dp[n][capacity]  # => the best achievable value at full capacity


def knapsack_1d_space_optimized(  # => same recurrence, but reuses ONE row via reverse order
    weights: list[int],  # => each item's own weight
    values: list[int],  # => each item's own value
    capacity: int,  # => item weights/values + limit
) -> int:  # => O(n * capacity) TIME, but only O(capacity) SPACE
    dp: list[int] = [0] * (capacity + 1)  # => ONE row instead of n+1 rows
    for i in range(len(weights)):  # => processes each item once
        w, v = weights[i], values[i]  # => this item's own weight/value
        for c in range(
            capacity,  # => starts from full capacity
            w - 1,  # => stops just short of this item's own weight
            -1,  # => steps backward -- THE KEY TRICK
        ):  # => THE KEY TRICK: iterates capacity DOWNWARD, not upward
            dp[c] = max(
                dp[c],  # => the SKIP option's value, still last item's
                v + dp[c - w],  # => the TAKE option's value
            )  # => dp[c-w] here is still the PREVIOUS item's value (not yet overwritten)
    return dp[capacity]  # => same final answer, using far less memory


# => the same 4-item instance as Example 51, so the two answers can be compared directly
weights: list[int] = [2, 3, 4, 5]  # => the same instance as Example 51
values: list[int] = [3, 4, 5, 6]  # => their corresponding values
capacity = 5  # => the knapsack's weight limit
full_table_answer = knapsack_2d_full_table(  # => opens the full-table call
    weights,  # => same weights as the space-optimized call below
    values,  # => same values as the space-optimized call below
    capacity,  # => same inputs as the space-optimized version
)  # => O(n*cap) space
space_optimized_answer = knapsack_1d_space_optimized(  # => opens the 1D-DP call
    weights,  # => same weights as the full-table call above
    values,  # => same values as the full-table call above
    capacity,  # => same inputs as the full-table version
)  # => O(cap) space
print(full_table_answer)  # => Output: 7
print(space_optimized_answer)  # => Output: 7

# confirms the space-optimized 1D pass agrees exactly with the full 2D table
assert full_table_answer == space_optimized_answer  # => confirms IDENTICAL results
assert space_optimized_answer == 7  # => confirms it matches Example 51's known answer
print("ex-62 OK")  # => Output: ex-62 OK
