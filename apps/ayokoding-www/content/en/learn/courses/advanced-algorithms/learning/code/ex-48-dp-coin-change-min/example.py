"""Example 48: Minimum-Coin Change via DP -- Beats Example 45's Greedy Answer."""

# dp[a] = minimum coins to make amount a (co-23): try EVERY coin as the LAST
# one used, and take the best option -- this explores possibilities greedy
# never considers, so it can't be fooled the way Example 45's greedy was.
INF = float("inf")  # => sentinel for "no way to make this amount (yet)"


def min_coins_dp(  # => tries every coin as the LAST one used, keeps the best count
    coins: list[int],
    amount: int,  # => the available coin denominations, and the target
) -> int | None:  # => None if amount is unreachable with these coins
    dp: list[float] = [0.0] + [  # => opens the dp array construction
        INF  # => every amount besides 0 starts as "not yet known reachable"
    ] * amount  # => dp[0]=0 coins; everything else unknown
    for a in range(  # => opens the ascending-amount range
        1,
        amount + 1,  # => builds every amount from 1 up to the target, in order
    ):  # => builds dp[a] from smaller, already-solved amounts
        for c in coins:  # => tries EVERY coin as the one used LAST to reach amount a
            if (  # => opens the "coin c improves dp[a]" check
                c <= a and dp[a - c] + 1 < dp[a]
            ):  # => using coin c beats the current best
                dp[a] = (  # => opens the improved-count assignment
                    dp[a - c] + 1  # => one more coin on top of the best way to make a-c
                )  # => one more coin than however dp[a-c] was reached
    return (  # => opens the final unreachable-or-int-result decision
        None if dp[amount] == INF else int(dp[amount])  # => still INF means unreachable
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
