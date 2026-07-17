"""Example 51: 0/1 Knapsack -- 2D DP over Items and Capacity."""

# dp[i][w] = best value using the first i items within capacity w (co-24):
# for each item, either SKIP it (dp[i-1][w]) or TAKE it (its value plus
# dp[i-1][w-weight], if it fits) -- "0/1" because each item is taken at
# most once, unlike the unbounded knapsack variant.


def knapsack_01(  # => for each item, either SKIP it or TAKE it, whichever is better
    weights: list[int],  # => each item's own weight
    values: list[int],  # => each item's own value
    capacity: int,  # => item weights/values + limit
) -> int:  # => O(n * capacity) time and space
    n = len(weights)  # => number of available items
    dp: list[list[int]] = [  # => opens the 2D table construction
        [0] * (capacity + 1)  # => one zero-filled row per item count
        for _ in range(n + 1)  # => one fresh row of zeros per item count
    ]  # => dp[0][*] = 0: zero items always yields zero value
    for i in range(1, n + 1):  # => considers items one at a time
        weight, value = weights[i - 1], values[i - 1]  # => this item's own weight/value
        for w in range(capacity + 1):  # => every possible capacity, from 0 up
            dp[i][w] = dp[i - 1][w]  # => the SKIP option: value stays whatever it was
            if weight <= w:  # => the TAKE option is only possible if it actually fits
                dp[i][w] = max(
                    dp[i][w],  # => the SKIP option's value
                    value + dp[i - 1][w - weight],  # => the TAKE option's value
                )  # => best of skip vs take
    return dp[n][capacity]  # => the best achievable value at full capacity


weights: list[int] = [2, 3, 4, 5]  # => four items' weights
values: list[int] = [3, 4, 5, 6]  # => their corresponding values
capacity = 5  # => the knapsack's weight limit
best_value = knapsack_01(weights, values, capacity)  # => the optimal achievable value
print(best_value)  # => Output: 7 -- items 0 and 1 (weight 2+3=5, value 3+4=7)

assert best_value == 7  # => confirms the known optimal value for this instance
assert knapsack_01([], [], 10) == 0  # => no items at all -- nothing to gain
assert (  # => opens the too-heavy-item check
    knapsack_01([100], [50], 1) == 0  # => True only if the DP correctly skips it
)  # => an item too heavy to ever fit contributes nothing
print("ex-51 OK")  # => Output: ex-51 OK
