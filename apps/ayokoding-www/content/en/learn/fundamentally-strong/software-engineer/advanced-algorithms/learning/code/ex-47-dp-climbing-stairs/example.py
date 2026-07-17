"""Example 47: Count Ways to Climb n Stairs (1 or 2 Steps at a Time) via DP."""

# ways(n) = ways(n-1) + ways(n-2) (co-23): the LAST step taken to reach stair
# n was either a 1-step from stair n-1, or a 2-step from stair n-2 -- so the
# total ways to reach n is simply the sum of ways to reach each predecessor.
# This is structurally IDENTICAL to Fibonacci, just with different seed values.


def count_ways_to_climb(  # => Fibonacci-shaped recurrence, computed bottom-up
    n: int,  # => the target stair count
) -> int:  # => bottom-up tabulation, O(n) time, O(1) space
    if n <= 1:  # => 0 stairs: 1 way (do nothing); 1 stair: 1 way (a single 1-step)
        return 1  # => base cases
    prev2, prev1 = 1, 1  # => ways(0)=1, ways(1)=1 -- the two seeds
    for _ in range(2, n + 1):  # => builds ways(i) from the two steps before it
        prev2, prev1 = (  # => opens the two-variable slide
            prev1,  # => the new prev2 -- what used to be prev1
            prev2 + prev1,  # => the new prev1 -- this stair's own way-count
        )  # => slides forward: ways(i) = ways(i-1)+ways(i-2)
    return prev1  # => ways(n)


def count_ways_brute_force(n: int) -> int:  # => O(2^n): enumerates every step sequence
    if n <= 1:  # => same base cases
        return 1  # => 0 or 1 stairs: exactly one way
    if n == 2:  # => exactly 2 ways: [1,1] or [2]
        return 2  # => the second base case
    return count_ways_brute_force(
        n - 1  # => recurses on the 1-step predecessor
    ) + count_ways_brute_force(  # => the LAST-step split
        n - 2  # => recurses on the 2-step predecessor
    )  # => no memoization -- deliberately re-derives the same recurrence, slowly


for n in [0, 1, 2, 3, 4, 5]:  # => a spread of small n, where brute force stays feasible
    fast = count_ways_to_climb(n)  # => O(n) tabulated answer
    slow = count_ways_brute_force(n)  # => O(2^n) brute-force answer, as ground truth
    print(f"n={n}: {fast}")  # => Output: one "n=N: ways" line per n
    assert fast == slow  # => confirms both approaches agree exactly

assert count_ways_to_climb(5) == 8  # => 1+1+1+1+1, 2+1+1+1 (x4 orderings), 2+2+1 (x3)
print("ex-47 OK")  # => Output: ex-47 OK
