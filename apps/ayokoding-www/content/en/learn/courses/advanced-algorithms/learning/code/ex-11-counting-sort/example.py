"""Example 11: Counting Sort -- O(n+k) for a Small, Known Range."""

# Counting sort (co-10) beats the comparison-sort O(n log n) lower bound by
# NOT comparing elements at all -- it counts occurrences of each possible
# value (range k) and reconstructs the sorted output directly. O(n+k) time.


def counting_sort(items: list[int], k: int) -> list[int]:  # => k = max value + 1
    counts: list[int] = [0] * k  # => counts[v] will hold how many times v appears
    for value in items:  # => O(n): tallies each value's frequency
        counts[value] += 1  # => increments the bucket for this exact value
    for i in range(1, k):  # => O(k): converts counts into a running prefix sum
        counts[i] += counts[i - 1]  # => counts[i] is now "how many values are <= i"
    result: list[int] = [0] * len(items)  # => pre-allocated output, same size as input
    for value in reversed(items):  # => walking BACKWARD keeps the sort stable (co-11)
        counts[value] -= 1  # => decrements first -- converts a count to a 0-based index
        result[counts[value]] = value  # => places value at its final sorted position
    return result  # => the fully sorted output, built without a single comparison


data: list[int] = [4, 2, 2, 8, 3, 3, 1, 0]  # => small integers, range 0..8
sorted_data = counting_sort(data, k=9)  # => k=9 covers values 0 through 8
print(sorted_data)  # => Output: [0, 1, 2, 2, 3, 3, 4, 8]

assert sorted_data == [0, 1, 2, 2, 3, 3, 4, 8]  # => confirms correct ascending order
assert sorted_data == sorted(data)  # => confirms it matches Python's own sort too
assert counting_sort([], k=1) == []  # => confirms the empty-input edge case
print("ex-11 OK")  # => Output: ex-11 OK
