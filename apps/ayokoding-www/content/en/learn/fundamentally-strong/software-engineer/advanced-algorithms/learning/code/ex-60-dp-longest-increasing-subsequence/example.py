"""Example 60: Longest Increasing Subsequence -- O(n^2) DP vs O(n log n) Patience."""

# dp[i] = length of the LIS ENDING at index i (co-23): look back at every
# earlier smaller element and extend its best LIS by one. The patience-
# sorting variant (co-27) instead maintains the smallest possible "tail"
# value for each achievable LIS length, using BINARY SEARCH to place each
# new element -- same final answer, but O(n log n) instead of O(n^2).
import bisect


def lis_length_dp(items: list[int]) -> int:  # => O(n^2): the straightforward DP
    if not items:  # => an empty sequence has LIS length 0
        return 0
    dp: list[int] = [1] * len(
        items
    )  # => every element is, at minimum, its own LIS of 1
    for i in range(len(items)):  # => for each position...
        for j in range(i):  # => ...checks every EARLIER position
            if items[j] < items[i]:  # => items[i] could extend an increasing run from j
                dp[i] = max(
                    dp[i], dp[j] + 1
                )  # => extends j's best LIS by one, if better
    return max(dp)  # => the longest LIS ending anywhere


def lis_length_patience(
    items: list[int],
) -> int:  # => O(n log n): binary-search variant
    tails: list[int] = []  # => tails[k] = smallest possible tail of a length-(k+1) LIS
    for x in items:  # => processes elements left to right, one at a time
        pos = bisect.bisect_left(
            tails, x
        )  # => O(log n): where x would insert to keep tails sorted
        if pos == len(tails):  # => x is bigger than every current tail -- LIS GROWS
            tails.append(x)  # => extends the longest LIS found so far by one
        else:  # => x can replace an existing tail with a SMALLER one, same length
            tails[pos] = x  # => keeps future extensions as easy as possible
    return len(
        tails
    )  # => the final length -- tails' VALUES are not the actual sequence


sequence: list[int] = [
    10,
    9,
    2,
    5,
    3,
    7,
    101,
    18,
]  # => the classic LeetCode LIS example
dp_answer = lis_length_dp(sequence)  # => O(n^2) DP result
patience_answer = lis_length_patience(sequence)  # => O(n log n) patience-sort result
print(dp_answer)  # => Output: 4
print(patience_answer)  # => Output: 4 -- e.g. [2, 3, 7, 101] or [2, 3, 7, 18]

assert dp_answer == patience_answer  # => confirms both approaches agree exactly
assert dp_answer == 4  # => confirms the known LIS length for this classic example
assert lis_length_dp([]) == 0  # => confirms the empty-sequence edge case
print("ex-60 OK")  # => Output: ex-60 OK
