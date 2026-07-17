"""Example 79: 0/1 Knapsack -- Brute Force vs Greedy vs DP, and Where They Cross."""

# The SAME problem (0/1 knapsack) solved three ways exposes each paradigm's
# tradeoff (co-05, co-22, co-23): brute force is always correct but O(2^n);
# greedy is fast but can be WRONG (no exchange-argument proof applies here);
# DP trades memory for a GUARANTEE of correctness at O(n * capacity). Step
# counts (not wall-clock) reveal exactly where DP overtakes brute force.


def brute_force_knapsack(
    weights: list[int], values: list[int], capacity: int
) -> tuple[int, int]:  # => (best value, subsets examined) -- tries EVERY subset
    n = len(weights)
    best = 0
    states_examined = 0
    for mask in range(1 << n):  # => 2^n possible subsets -- the exhaustive search space
        states_examined += 1
        total_weight = 0
        total_value = 0
        for i in range(n):
            if mask & (1 << i):  # => bit i set means "item i is in this subset"
                total_weight += weights[i]
                total_value += values[i]
        if total_weight <= capacity and total_value > best:
            best = total_value  # => tracks the best FEASIBLE subset found
    return best, states_examined


def greedy_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    # => sorts by value-per-weight ratio, then takes GREEDILY -- O(n log n), no guarantee
    n = len(weights)
    order = sorted(
        range(n), key=lambda i: values[i] / weights[i], reverse=True
    )  # => best ratio first
    total_weight = 0
    total_value = 0
    for i in order:
        if total_weight + weights[i] <= capacity:  # => takes it if it still fits
            total_weight += weights[i]
            total_value += values[i]
    return total_value  # => NO optimality guarantee -- unlike fractional knapsack


def dp_knapsack(
    weights: list[int], values: list[int], capacity: int
) -> tuple[int, int]:  # => (best value, table cells filled) -- ALWAYS optimal
    n = len(weights)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]  # => O(n * capacity) space
    cells_filled = 0
    for i in range(1, n + 1):
        for c in range(capacity + 1):
            cells_filled += 1
            if weights[i - 1] <= c:  # => item i-1 fits within capacity c
                table[i][c] = max(
                    table[i - 1][c],  # => option A: skip item i-1
                    table[i - 1][c - weights[i - 1]]
                    + values[i - 1],  # => option B: take it
                )
            else:
                table[i][c] = table[i - 1][c]  # => too heavy -- forced to skip
    return table[n][capacity], cells_filled


# A textbook 0/1 knapsack instance where greedy DEMONSTRABLY fails: the
# best ratio item (60/10=6.0) locks in capacity that the true optimal pair
# needed instead.
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
brute_best, _ = brute_force_knapsack(weights, values, capacity)
dp_best, _ = dp_knapsack(weights, values, capacity)
greedy_best = greedy_knapsack(weights, values, capacity)
print(
    brute_best
)  # => Output: 220 -- items 1+2 (weight 50, value 220): the true optimum
print(dp_best)  # => Output: 220 -- DP matches brute force exactly, but polynomial work
print(
    greedy_best
)  # => Output: 160 -- greedy locks in item 0 early and MISSES the optimum

assert (
    brute_best == dp_best == 220
)  # => confirms DP achieves the SAME optimum as brute force
assert greedy_best < brute_best  # => confirms greedy is genuinely SUBOPTIMAL here

# Now the "shootout": as n grows, does brute force's 2^n outgrow DP's n*capacity?
crossover_seen = False
for n in (4, 8, 12, 16, 20):  # => a growing item count, fixed capacity
    grown_weights = [
        ((i * 3) % 9) + 2 for i in range(n)
    ]  # => deterministic synthetic items
    grown_values = [((i * 7 + 3) % 20) + 1 for i in range(n)]
    _, brute_states = brute_force_knapsack(grown_weights, grown_values, capacity)
    _, dp_cells = dp_knapsack(grown_weights, grown_values, capacity)
    if n == 8:
        assert (
            brute_states < dp_cells
        )  # => at n=8, brute force is STILL cheaper (256 < 408)
    if n == 12:
        assert (
            brute_states > dp_cells
        )  # => at n=12, brute force has CROSSED OVER (4096 > 612)
        crossover_seen = True

assert crossover_seen  # => confirms the paradigm crossover was actually observed
print("ex-79 OK")  # => Output: ex-79 OK
