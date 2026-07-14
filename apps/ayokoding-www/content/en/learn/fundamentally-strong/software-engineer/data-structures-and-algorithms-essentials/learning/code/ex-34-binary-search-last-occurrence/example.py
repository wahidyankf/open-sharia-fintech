"""Example 34: Binary Search -- Rightmost (Last) Occurrence."""


# Mirror image of Example 33: keeps searching RIGHT after a match (co-14).
def find_last(items: list[int], target: int) -> int:  # => a plain iterative function
    low, high = 0, len(items) - 1  # => the inclusive range still being searched
    result = -1  # => tracks the best (rightmost) match found so far
    while low <= high:  # => O(log n) -- same shape as find_first, mirrored
        mid = (low + high) // 2  # => the midpoint of the current range
        if (
            items[mid] == target
        ):  # => a candidate match -- but maybe not the rightmost one
            result = mid  # => record this match...
            low = mid + 1  # => ...then keep searching the RIGHT half for a later one
        elif items[mid] < target:  # => the midpoint is too small
            low = mid + 1  # => target must be further right
        else:  # => the midpoint is too large
            high = mid - 1  # => target must be further left
    return result  # => the largest index where target was ever recorded


duplicates = [1, 2, 2, 2, 3, 4]  # => target 2 appears at indices 1, 2, and 3
last_index = find_last(duplicates, 2)  # => the rightmost occurrence is index 3
print(last_index)  # => Output: 3

assert (
    last_index == 3
)  # => confirms the rightmost occurrence, not the first match found
print("ex-34 OK")  # => Output: ex-34 OK
