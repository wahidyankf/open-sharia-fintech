"""Example 79: 0/1 Knapsack -- Brute Force vs Greedy vs DP, and Where They Cross."""

# The SAME problem (0/1 knapsack) solved three ways exposes each paradigm's
# tradeoff (co-05, co-22, co-23): brute force is always correct but O(2^n);
# greedy is fast but can be WRONG (no exchange-argument proof applies here);
# DP trades memory for a GUARANTEE of correctness at O(n * capacity). Step
# counts (not wall-clock) reveal exactly where DP overtakes brute force.


def brute_force_knapsack(  # => tries every one of the 2^n subsets, keeps the best feasible one
    weights: list[int],  # => each item's own weight
    values: list[int],  # => each item's own value
    capacity: int,  # => item weights/values + limit
) -> tuple[int, int]:  # => (best value, subsets examined) -- tries EVERY subset
    n = len(weights)  # => number of available items
    best = 0  # => the best feasible value found so far
    states_examined = 0  # => counts every subset (bitmask) tried
    for mask in range(1 << n):  # => 2^n possible subsets -- the exhaustive search space
        states_examined += 1  # => one more subset examined
        total_weight = 0  # => this subset's combined weight
        total_value = 0  # => this subset's combined value
        for i in range(n):  # => checks each item's bit within this subset's mask
            if mask & (1 << i):  # => bit i set means "item i is in this subset"
                total_weight += weights[i]  # => adds item i's weight
                total_value += values[i]  # => adds item i's value
        if (  # => opens the feasible-and-better check
            total_weight <= capacity and total_value > best
        ):  # => feasible AND strictly better
            best = total_value  # => tracks the best FEASIBLE subset found
    return best, states_examined  # => the true optimum, plus how much work it took


def greedy_knapsack(  # => sorts by value-per-weight ratio, then takes GREEDILY
    weights: list[int], values: list[int], capacity: int
) -> int:  # => fast, unproven
    # => sorts by value-per-weight ratio, then takes GREEDILY -- O(n log n), no guarantee
    n = len(weights)  # => number of available items
    order = sorted(  # => opens the ratio-sort call
        range(n),  # => item indices, sorted by their own ratio
        key=lambda i: values[i] / weights[i],
        reverse=True,  # => best ratio first
    )  # => best ratio first
    total_weight = 0  # => running greedy weight total
    total_value = 0  # => running greedy value total
    for i in order:  # => tries each item, best ratio first
        if total_weight + weights[i] <= capacity:  # => takes it if it still fits
            total_weight += weights[i]  # => commits its weight
            total_value += values[i]  # => commits its value
    return total_value  # => NO optimality guarantee -- unlike fractional knapsack


def dp_knapsack(  # => fills a 2D table bottom-up, guaranteed globally optimal
    weights: list[int],  # => each item's own weight
    values: list[int],  # => each item's own value
    capacity: int,  # => item weights/values + limit
) -> tuple[int, int]:  # => (best value, table cells filled) -- ALWAYS optimal
    n = len(weights)  # => number of available items
    table = [[0] * (capacity + 1) for _ in range(n + 1)]  # => O(n * capacity) space
    cells_filled = 0  # => counts every DP table cell computed
    for i in range(1, n + 1):  # => considers items one at a time
        for c in range(capacity + 1):  # => every possible capacity, from 0 up
            cells_filled += 1  # => one more cell computed
            if weights[i - 1] <= c:  # => item i-1 fits within capacity c
                table[i][c] = max(  # => opens the skip-vs-take comparison
                    table[i - 1][c],  # => option A: skip item i-1
                    table[i - 1][
                        c - weights[i - 1]  # => leftover capacity after taking item
                    ]  # => opens option B's own value lookup
                    + values[i - 1],  # => option B: take it
                )  # => closes the max(skip, take) comparison
            else:  # => item i-1 is too heavy for capacity c
                table[i][c] = table[i - 1][c]  # => too heavy -- forced to skip
    return table[n][
        capacity  # => the final answer: n items, full capacity available
    ], cells_filled  # => the true optimum, plus how much work it took


# A textbook 0/1 knapsack instance where greedy DEMONSTRABLY fails: the
# best ratio item (60/10=6.0) locks in capacity that the true optimal pair
# needed instead.
# => a textbook counterexample where the best-ratio item locks in capacity suboptimally
weights = [10, 20, 30]  # => three items' weights
values = [60, 100, 120]  # => their corresponding values -- ratios 6.0, 5.0, 4.0
capacity = 50  # => the knapsack's weight limit
brute_best, _ = brute_force_knapsack(  # => opens the guaranteed-optimal run
    weights, values, capacity
)  # => the guaranteed optimum
dp_best, _ = dp_knapsack(weights, values, capacity)  # => the DP's own optimum
greedy_best = greedy_knapsack(  # => opens the fast-but-unproven run
    weights, values, capacity
)  # => the greedy heuristic's answer
print(  # => opens the guaranteed-optimal-value print call
    brute_best  # => the guaranteed-optimal value, for comparison
)  # => Output: 220 -- items 1+2 (weight 50, value 220): the true optimum
print(dp_best)  # => Output: 220 -- DP matches brute force exactly, but polynomial work
print(  # => opens the greedy-result print call
    greedy_best  # => the greedy heuristic's own (suboptimal) value
)  # => Output: 160 -- greedy locks in item 0 early and MISSES the optimum

assert (  # => opens the brute-force-and-DP-agree check
    brute_best == dp_best == 220  # => both exhaustive AND DP agree on the true optimum
)  # => confirms DP achieves the SAME optimum as brute force
assert greedy_best < brute_best  # => confirms greedy is genuinely SUBOPTIMAL here

# Now the "shootout": as n grows, does brute force's 2^n outgrow DP's n*capacity?
# => tracks whether the shootout actually observed brute force overtaking DP in cost
crossover_seen = False  # => flips True once brute force is caught overtaking DP
for n in (4, 8, 12, 16, 20):  # => a growing item count, fixed capacity
    grown_weights = [  # => opens the deterministic synthetic-weights comprehension
        ((i * 3) % 9) + 2  # => a repeatable, bounded pseudo-random weight per item
        for i in range(n)  # => a repeatable, bounded pseudo-random weight
    ]  # => deterministic synthetic items
    grown_values = [  # => opens the deterministic synthetic-values comprehension
        ((i * 7 + 3) % 20) + 1 for i in range(n)
    ]  # => deterministic synthetic values
    _, brute_states = brute_force_knapsack(  # => opens the brute-force benchmark run
        grown_weights, grown_values, capacity
    )  # => 2^n subsets
    _, dp_cells = dp_knapsack(  # => opens the DP benchmark run
        grown_weights, grown_values, capacity
    )  # => n*capacity cells
    if n == 8:  # => a checkpoint BEFORE the expected crossover
        assert (  # => opens the pre-crossover assertion
            brute_states < dp_cells  # => brute force is still the cheaper option here
        )  # => at n=8, brute force is STILL cheaper (256 < 408)
    if n == 12:  # => a checkpoint AFTER the expected crossover
        assert (  # => opens the post-crossover assertion
            brute_states  # => the 2^n subset count at this larger n
            > dp_cells  # => brute force has now become the MORE expensive option
        )  # => at n=12, brute force has CROSSED OVER (4096 > 612)
        crossover_seen = True  # => records that the crossover was genuinely observed

assert crossover_seen  # => confirms the paradigm crossover was actually observed
print("ex-79 OK")  # => Output: ex-79 OK
