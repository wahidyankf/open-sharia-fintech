"""Example 48: Minimum-Coin Change via DP -- Beats Example 45's Greedy Answer."""

# dp[a] = minimum coins to make amount a (co-23): try EVERY coin as the LAST
# one used, and take the best option -- this explores possibilities greedy
# never considers, so it can't be fooled the way Example 45's greedy was.
INF = float("inf")  # => sentinel for "no way to make this amount (yet)"


def min_coins_dp(
    coins: list[int], amount: int
) -> int | None:  # => None if amount is unreachable with these coins
    dp: list[float] = [0.0] + [
        INF
    ] * amount  # => dp[0]=0 coins; everything else unknown
    for a in range(
        1, amount + 1
    ):  # => builds dp[a] from smaller, already-solved amounts
        for c in coins:  # => tries EVERY coin as the one used LAST to reach amount a
            if (
                c <= a and dp[a - c] + 1 < dp[a]
            ):  # => using coin c beats the current best
                dp[a] = (
                    dp[a - c] + 1
                )  # => one more coin than however dp[a-c] was reached
    return (
        None if dp[amount] == INF else int(dp[amount])
    )  # => None if truly unreachable


non_canonical_coins: list[int] = [1, 3, 4]  # => Example 45's counterexample coin set
target = 6  # => the same target Example 45 used
result = min_coins_dp(non_canonical_coins, target)  # => the TRUE minimum via DP
print(result)  # => Output: 2 -- two 3-coins: 3 + 3 = 6

assert result == 2  # => confirms DP finds the true optimum
assert result < 3  # => confirms DP strictly BEATS Example 45's greedy answer (3 coins)
assert min_coins_dp([1, 3, 4], 0) == 0  # => zero coins are needed to make amount 0
assert min_coins_dp([5], 3) is None  # => 3 is unreachable using only 5-coins
print("ex-48 OK")  # => Output: ex-48 OK
