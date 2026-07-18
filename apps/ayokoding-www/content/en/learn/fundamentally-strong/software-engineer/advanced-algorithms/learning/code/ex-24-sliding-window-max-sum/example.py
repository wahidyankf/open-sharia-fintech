"""Example 24: Maximum Sum of a Fixed-Size Sliding Window, O(n) vs Brute Force."""

# A sliding window (co-26) reuses the PREVIOUS window's sum: slide one step by
# subtracting the element that just left and adding the one that just entered
# -- O(1) per step, O(n) total -- instead of re-summing all k elements each time.


def brute_force_max_window_sum(  # => the naive baseline, used only to check correctness
    items: list[int],
    k: int,  # => the data and the fixed window width
) -> int:  # => O(n*k): re-sums every window from scratch
    best = sum(items[:k])  # => the first window's sum, as a starting baseline
    for start in range(1, len(items) - k + 1):  # => tries every other window position
        window_sum = sum(items[start : start + k])  # => O(k): a full re-sum each time
        best = max(best, window_sum)  # => keeps the largest sum seen so far
    return best  # => the maximum sum over any k-length window


def sliding_window_max_sum(  # => the O(n) fast path, reusing the previous window's sum
    items: list[int],
    k: int,  # => same signature as the brute-force version above
) -> int:  # => O(n): each element enters and leaves the window exactly once
    window_sum = sum(items[:k])  # => O(k), but only ONCE -- the very first window
    best = window_sum  # => tracks the best sum found so far
    for i in range(k, len(items)):  # => slides the window one step at a time
        window_sum += (  # => updates the running sum in constant time, no re-summing
            items[i] - items[i - k]  # => net change: new element in, old element out
        )  # => O(1): add the entering element, drop the leaving one
        best = max(best, window_sum)  # => updates the running maximum
    return best  # => the maximum sum over any k-length window


data: list[int] = [2, 1, 5, 1, 3, 2, 7, 1]  # => 8 integers
k = 3  # => window size
brute_result = brute_force_max_window_sum(data, k)  # => O(n*k) ground truth
fast_result = sliding_window_max_sum(data, k)  # => O(n) sliding-window answer
print(brute_result)  # => Output: 12
print(fast_result)  # => Output: 12

assert brute_result == fast_result  # => confirms both approaches agree exactly
assert fast_result == 12  # => the window [3, 2, 7] (indices 4-6) sums to 12, the max
print("ex-24 OK")  # => Output: ex-24 OK
