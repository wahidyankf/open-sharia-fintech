"""Example 60: Maximum Sum of a Length-k Sliding Window."""


# Slides a fixed-size window, updating the sum incrementally -- O(n),
# instead of re-summing each window from scratch, which would be O(n*k) (co-20).
def max_window_sum(
    values: list[int], k: int
) -> int:  # => a plain sliding-window function
    window_sum = sum(values[:k])  # => O(k): the sum of the FIRST window only
    best = window_sum  # => tracks the best sum seen so far
    for i in range(k, len(values)):  # => slides the window one element at a time
        window_sum += (
            values[i] - values[i - k]
        )  # => add the new element, drop the old one
        # => this single O(1) update replaces re-summing k elements from scratch
        best = max(best, window_sum)  # => keep the running maximum
    return best  # => the maximum window sum found across every position


numbers = [2, 1, 5, 1, 3, 2]  # => 6 values; window size 3
result = max_window_sum(
    numbers, 3
)  # => windows: [2,1,5]=8, [1,5,1]=7, [5,1,3]=9, [1,3,2]=6
print(result)  # => Output: 9

assert result == 9  # => confirms the best window (index 2..4: 5+1+3) was found
print("ex-60 OK")  # => Output: ex-60 OK
