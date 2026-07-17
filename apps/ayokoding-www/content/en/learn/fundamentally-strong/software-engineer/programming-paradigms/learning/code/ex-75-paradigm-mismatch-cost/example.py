"""Example 75: Paradigm Mismatch Cost."""

import inspect  # => used only to MEASURE source length below -- not part of either search's own logic
from itertools import product  # => generates every (i, j, k) candidate for the constraint-declared version

TARGET_SUM = 15  # => shared search target for both versions -- three distinct digits must sum to this


def solve_imperative_painfully(digits: list[int]) -> tuple[int, int, int] | None:  # => search via brute nested loops
    # => find three DISTINCT digits from the list whose sum is 15 -- written the "obvious" imperative way
    for i in range(len(digits)):  # => manual triple-nested loop -- exactly the shape constraint programming avoids
        for j in range(len(digits)):  # => nested loop level 2
            if j == i:  # => manual distinctness check #1
                continue  # => skip this (i, j) pair -- reused index, not a valid triple
            for k in range(len(digits)):  # => nested loop level 3
                if k == i or k == j:  # => manual distinctness check #2, repeated for the third index
                    continue  # => skip this (i, j, k) triple -- reused index, not a valid triple
                if digits[i] + digits[j] + digits[k] == TARGET_SUM:  # => the sum check, buried inside three nested loops
                    return (digits[i], digits[j], digits[k])  # => first valid triple found, in loop order
    return None  # => no valid triple exists in this digit list


def solve_with_constraints(digits: list[int]) -> tuple[int, int, int] | None:  # => the SAME search, declared
    for combo in product(range(len(digits)), repeat=3):  # => still generates candidates, but...
        i, j, k = combo  # => unpack the candidate triple of indices
        if len({i, j, k}) == 3 and digits[i] + digits[j] + digits[k] == TARGET_SUM:  # => the constraints ARE the logic
            return (digits[i], digits[j], digits[k])  # => "distinct AND sums to 15" reads as one condition
    return None  # => no valid triple exists in this digit list


digits = [1, 4, 5, 6, 9, 10]  # => shared search space for both versions
painful = solve_imperative_painfully(digits)  # => run the nested-loop version
clean = solve_with_constraints(digits)  # => run the constraint-declared version
assert painful is not None  # => narrow away None -- this digit list always has a valid triple
assert clean is not None  # => narrow away None -- same search space, so the same guarantee holds

print(painful)  # => both must find A valid triple summing to 15 (not necessarily the SAME triple)
# => Output: (1, 4, 10)
print(clean)  # => the constraint-style search happens to try combos in the same order here
# => Output: (1, 4, 10)
print(sum(painful) == sum(clean) == 15)  # => both are CORRECT, regardless of which specific triple each finds
# => Output: True

painful_lines = len(inspect.getsource(solve_imperative_painfully).strip().splitlines())  # => measured, not guessed
clean_lines = len(inspect.getsource(solve_with_constraints).strip().splitlines())  # => measured, not guessed
print(painful_lines, clean_lines)  # => the nested-loop version needs more lines for the same search
# => Output: 12 6
