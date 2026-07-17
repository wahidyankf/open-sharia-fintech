"""Example 58: 0/1 Knapsack -- Greedy by Value/Weight Ratio Diverges from DP-Optimal."""

# Fractional knapsack's greedy-by-ratio is provably optimal WHEN items can be
# split. Forced to take items WHOLE (0/1, co-22), that same greedy heuristic
# can strand capacity that a globally-optimal DP (co-23) would have used
# better -- the greedy-choice property that makes fractional-knapsack work
# simply does not transfer to the 0/1 variant.


def greedy_knapsack_by_ratio(  # => sorts by value/weight ratio, then takes greedily
    weights: list[int],  # => each item's own weight
    values: list[int],  # => each item's own value
    capacity: int,  # => item weights/values + limit
) -> int:  # => O(n log n): sorts by ratio, then takes whole items greedily
    items = sorted(  # => opens the ratio-sort call
        zip(weights, values),  # => pairs each item's weight with its value
        key=lambda pair: pair[1] / pair[0],  # => sorts by value-per-weight ratio
        reverse=True,  # => best ratio first
    )  # => highest value-per-weight first
    total_value = 0  # => running greedy total
    remaining = capacity  # => how much capacity is still unused
    for w, v in items:  # => tries each item, best ratio first
        if w <= remaining:  # => it fits WHOLE -- take it (no fractions allowed)
            total_value += v  # => adds its full value
            remaining -= w  # => consumes its full weight
        # => else: SKIPPED ENTIRELY -- no partial credit, unlike fractional knapsack
    return total_value  # => greedy's answer -- NOT guaranteed optimal for 0/1


def knapsack_01_dp(  # => the same 2D DP as Example 51, guaranteed globally optimal
    weights: list[int],  # => each item's own weight
    values: list[int],  # => each item's own value
    capacity: int,  # => item weights/values + limit
) -> int:  # => O(n * capacity): the same DP as Example 51, the true optimum
    n = len(weights)  # => number of available items
    dp: list[list[int]] = [
        [0] * (capacity + 1)  # => one zero-filled row per item count
        for _ in range(n + 1)
    ]  # => table of zeros
    for i in range(1, n + 1):  # => considers items one at a time
        w, v = weights[i - 1], values[i - 1]  # => this item's own weight/value
        for c in range(capacity + 1):  # => every possible capacity, from 0 up
            dp[i][c] = dp[i - 1][c]  # => the SKIP option: value stays whatever it was
            if w <= c:  # => the TAKE option is only possible if it actually fits
                dp[i][c] = max(
                    dp[i][c],  # => the SKIP option's value
                    v + dp[i - 1][c - w],  # => the TAKE option's value
                )  # => best of skip vs take
    return dp[n][capacity]  # => the true optimal value, considering EVERY combination


weights: list[int] = [10, 20, 30]  # => a classic textbook counterexample
values: list[int] = [60, 100, 120]  # => ratios: 6.0, 5.0, 4.0 -- item 0 looks best
capacity = 50  # => the knapsack's weight limit
greedy_answer = greedy_knapsack_by_ratio(  # => opens the greedy call
    weights,  # => same weights as the DP call below
    values,  # => same values as the DP call below
    capacity,  # => same inputs as the DP, for a fair comparison
)  # => takes item 0 (ratio 6), then item 1 (ratio 5); item 2 no longer fits
optimal_answer = knapsack_01_dp(weights, values, capacity)  # => the TRUE optimum
print(greedy_answer)  # => Output: 160 -- items 0 and 1: weight 30, value 160
print(optimal_answer)  # => Output: 220 -- items 1 and 2: weight 50, value 220

assert greedy_answer == 160  # => confirms greedy's (suboptimal) answer
assert optimal_answer == 220  # => confirms DP's true optimum
assert (  # => opens the greedy-underperforms-DP check
    optimal_answer > greedy_answer
)  # => confirms the greedy heuristic genuinely underperforms DP here
print("ex-58 OK")  # => Output: ex-58 OK
