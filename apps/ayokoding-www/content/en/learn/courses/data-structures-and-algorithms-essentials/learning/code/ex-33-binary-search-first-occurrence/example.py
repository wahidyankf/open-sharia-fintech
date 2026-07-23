"""Example 33: Binary Search -- Leftmost (First) Occurrence."""


# Keeps searching LEFT even after a match, to find the first duplicate (co-14).
def find_first(items: list[int], target: int) -> int:  # => a plain iterative function
    low, high = 0, len(items) - 1  # => the inclusive range still being searched
    result = -1  # => tracks the best (leftmost) match found so far
    while (
        low <= high
    ):  # => still O(log n) -- one extra comparison per step, not a rescan
        mid = (low + high) // 2  # => the midpoint of the current range
        if (
            items[mid] == target
        ):  # => a candidate match -- but maybe not the leftmost one
            result = mid  # => record this match...
            high = mid - 1  # => ...then keep searching the LEFT half for an earlier one
        elif items[mid] < target:  # => the midpoint is too small
            low = mid + 1  # => target must be further right
        else:  # => the midpoint is too large
            high = mid - 1  # => target must be further left
    return result  # => the smallest index where target was ever recorded


duplicates = [1, 2, 2, 2, 3, 4]  # => target 2 appears at indices 1, 2, and 3
first_index = find_first(duplicates, 2)  # => the leftmost occurrence is index 1
print(first_index)  # => Output: 1

assert first_index == 1  # => confirms the leftmost occurrence, not just any match
print("ex-33 OK")  # => Output: ex-33 OK
