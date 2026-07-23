"""Kata 7 (before): greedy coin change picks the largest coin first, which is SUBOPTIMAL on this coin set."""


def greedy_coin_change(coins: list[int], target: int) -> list[int]:
    result: list[int] = []
    remaining = target
    for coin in sorted(
        coins, reverse=True
    ):  # SMELL: "always take the biggest coin" has no optimality proof
        while remaining >= coin:
            result.append(coin)
            remaining -= coin
    return result


coins = [
    1,
    3,
    4,
]  # a NON-canonical coin set -- greedy's optimality only holds for specific coin systems
change = greedy_coin_change(coins, 6)
print(change)
print(len(change))
print(
    len(change) == 2
)  # optimal is [3, 3] -- 2 coins -- but greedy takes 4 first, forcing 4 + 1 + 1 = 3 coins
