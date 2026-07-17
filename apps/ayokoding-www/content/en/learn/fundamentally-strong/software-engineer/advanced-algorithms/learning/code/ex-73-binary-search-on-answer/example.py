"""Example 73: Binary Search on the Answer -- Minimum Ship Capacity Within D Days."""

# Binary-searching over a VALUE SPACE (co-27), not an array: "can capacity C
# ship everything within D days?" is MONOTONIC -- if C works, every LARGER
# capacity also works. That monotonicity is exactly what makes binary search
# valid here, hunting for the smallest C where the feasibility check flips.


def can_ship_within_days(  # => greedily packs, day by day, to test one candidate capacity
    weights: list[int],
    capacity: int,
    days: int,  # => packages, candidate capacity, day budget
) -> bool:  # => THE MONOTONIC PREDICATE being binary-searched
    days_needed = 1  # => at least one day is always needed
    current_load = 0  # => how much weight is loaded onto the CURRENT day's shipment
    for w in weights:  # => greedily packs each package onto the current day if it fits
        if current_load + w > capacity:  # => this package doesn't fit today
            days_needed += 1  # => starts a NEW day
            current_load = 0  # => resets the load for that new day
        current_load += w  # => adds this package to whichever day it landed on
    return days_needed <= days  # => True iff the greedy packing fits within the budget


def min_ship_capacity(  # => binary-searches the VALUE SPACE for the smallest feasible capacity
    weights: list[int],
    days: int,  # => packages to ship, and the day budget
) -> int:  # => O(n log(sum(weights)))
    lo = max(weights)  # => capacity must fit at LEAST the single heaviest package
    hi = sum(weights)  # => capacity never needs to exceed shipping everything in 1 day
    while lo < hi:  # => standard binary-search-on-answer bounds
        mid = (lo + hi) // 2  # => a CANDIDATE capacity to test
        if can_ship_within_days(weights, mid, days):  # => mid is FEASIBLE
            hi = mid  # => try to find an even SMALLER feasible capacity
        else:  # => mid is TOO SMALL -- infeasible
            lo = mid + 1  # => search strictly larger capacities only
    return lo  # => the smallest capacity for which the predicate is True


weights: list[int] = [  # => opens the classic LeetCode weights literal
    1,  # => package 0
    2,  # => package 1
    3,  # => package 2
    4,  # => package 3
    5,  # => package 4
    6,  # => package 5
    7,  # => package 6
    8,  # => package 7
    9,  # => package 8
    10,  # => package 9
]  # => the classic LeetCode example
result = min_ship_capacity(weights, days=5)  # => the smallest feasible ship capacity
print(result)  # => Output: 15

assert result == 15  # => confirms the known minimum capacity for this instance
assert can_ship_within_days(weights, result, 5) is True  # => confirms it's feasible
assert can_ship_within_days(weights, result - 1, 5) is False  # => the true BOUNDARY
print("ex-73 OK")  # => Output: ex-73 OK
