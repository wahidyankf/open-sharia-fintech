"""Example 65: Minimum Coins to Make Change, via Memoized Recursion."""

cache: dict[int, int] = {
    0: 0
}  # => base fact: 0 coins are needed to make amount 0 (co-19)


# Tries every coin as the "first" pick, recurses on the remainder, caches by amount (co-19, co-17).
def min_coins(
    coins: list[int], amount: int
) -> int:  # => a recursive function with a cache
    if amount in cache:  # => this exact remaining amount was already solved
        return cache[amount]  # => reuse the stored answer
    if amount < 0:  # => overshot -- this coin choice is invalid
        return -1  # => signal "impossible" for this branch
    best = -1  # => tracks the fewest coins found across all choices, or -1 if none work
    for coin in coins:  # => RECURSIVE CASE: try using this coin first
        sub_result = min_coins(
            coins, amount - coin
        )  # => solve the smaller remaining amount
        if sub_result != -1 and (
            best == -1 or sub_result + 1 < best
        ):  # => a better plan found
            best = (
                sub_result + 1
            )  # => this coin's plan beats the best plan found so far
    cache[amount] = best  # => memoize this amount's answer for any future call
    return best  # => the fewest coins needed for this amount, or -1 if impossible


coins = [1, 3, 4]  # => available denominations
result = min_coins(coins, 6)  # => best plan: 3 + 3 = two coins (not six 1s, not 4+1+1)
print(result)  # => Output: 2

assert (
    result == 2
)  # => confirms 3+3 (two coins) beats every other combination for amount 6
print("ex-65 OK")  # => Output: ex-65 OK
