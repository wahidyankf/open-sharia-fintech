"""Kata 7 (after): DP tries every coin at every amount, so it finds the true minimum regardless of coin set."""

import math


def dp_coin_change(coins: list[int], target: int) -> list[int]:
    # best[amount] = the fewest coins that sum to `amount`; best[0] = 0 coins, everything else starts at inf
    best: list[float] = [0.0] + [math.inf] * target
    choice: list[int] = [-1] * (target + 1)
    for amount in range(1, target + 1):
        for coin in coins:  # => tries EVERY coin, not just the biggest one -- no greedy assumption baked in
            if coin <= amount and best[amount - coin] + 1 < best[amount]:
                best[amount] = best[amount - coin] + 1
                choice[amount] = coin

    result: list[int] = []
    amount = target
    while amount > 0:
        result.append(choice[amount])
        amount -= choice[amount]
    return result


coins = [1, 3, 4]
change = dp_coin_change(coins, 6)
print(change)
print(len(change))
print(len(change) == 2)
