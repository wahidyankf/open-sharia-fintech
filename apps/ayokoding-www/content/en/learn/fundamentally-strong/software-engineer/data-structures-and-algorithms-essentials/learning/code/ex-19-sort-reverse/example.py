"""Example 19: sorted() with reverse=True."""

# reverse=True sorts descending -- Timsort's comparisons flip, cost stays O(n log n) (co-15).
values: list[int] = [4, 1, 8, 3]  # => an unsorted list of ints
descending = sorted(values, reverse=True)  # => largest first, smallest last
print(descending)  # => Output: [8, 4, 3, 1]

assert descending == [8, 4, 3, 1]  # => confirms strictly descending order
assert descending[0] == max(values)  # => confirms the largest value leads
assert descending[-1] == min(values)  # => confirms the smallest value trails
print("ex-19 OK")  # => Output: ex-19 OK
