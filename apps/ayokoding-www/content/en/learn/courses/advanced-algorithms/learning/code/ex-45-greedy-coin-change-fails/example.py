"""Example 45: Greedy Coin Change Fails on a Non-Canonical Coin Set."""

# Greedy (co-22) only works when the greedy-choice property actually HOLDS.
# US coins {1, 5, 10, 25} happen to make greedy-always-optimal, but that's a
# property of THIS SPECIFIC coin set, not of "greedy" in general (co-23):
# {1, 3, 4} is a counterexample where always taking the largest coin loses.


def greedy_coin_change(
    coins: list[int], amount: int
) -> list[int]:  # => always takes the LARGEST coin that still fits
    coins_sorted = sorted(coins, reverse=True)  # => tries biggest coins first
    used: list[int] = []  # => the coins greedily selected, in the order taken
    remaining = amount  # => how much of the target amount is still unpaid
    for c in coins_sorted:  # => tries each denomination, largest to smallest
        while remaining >= c:  # => keeps taking THIS coin as long as it still fits
            used.append(c)  # => records one more coin of this denomination
            remaining -= c  # => reduces the remaining amount accordingly
    return used  # => the greedy answer -- NOT guaranteed to be optimal


non_canonical_coins: list[int] = [1, 3, 4]  # => the counterexample coin set
target = 6  # => the amount to make change for
greedy_answer = greedy_coin_change(non_canonical_coins, target)  # => greedy's choice
print(greedy_answer)  # => Output: [4, 1, 1]
print(len(greedy_answer))  # => Output: 3 -- greedy needs 3 coins

optimal_answer: list[int] = [3, 3]  # => the TRUE optimum: two 3-coins, verified by hand
print(sum(optimal_answer) == target)  # => Output: True
print(len(optimal_answer))  # => Output: 2 -- strictly fewer coins than greedy found

assert sum(greedy_answer) == target  # => confirms greedy's answer is still VALID change
assert len(greedy_answer) == 3  # => confirms greedy's (suboptimal) coin count
assert len(optimal_answer) < len(
    greedy_answer
)  # => confirms a strictly BETTER answer exists that greedy never finds
print("ex-45 OK")  # => Output: ex-45 OK
