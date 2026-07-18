"""Example 52: Binary Search for the Leftmost and Rightmost Occurrence."""

# A plain binary search stops at ANY match. Finding the LEFTMOST (co-27)
# match instead means: on a match, don't stop -- keep searching the LEFT
# half for an even earlier one. The rightmost search is the mirror image.


def leftmost_index(items: list[int], target: int) -> int:  # => -1 if target is absent
    lo, hi = 0, len(items) - 1  # => the active search range
    result = -1  # => no match found yet
    while lo <= hi:  # => standard binary search bounds
        mid = (lo + hi) // 2  # => the midpoint of the active range
        if items[mid] == target:  # => found A match -- but is it the FIRST one?
            result = mid  # => records this as the best-known leftmost match so far
            hi = mid - 1  # => keeps searching LEFT for an even earlier occurrence
        elif items[mid] < target:  # => target must be further right
            lo = mid + 1  # => shrinks the range from the left edge
        else:  # => target must be further left
            hi = mid - 1  # => shrinks the range from the right edge
    return result  # => the smallest index where target occurs, or -1


def rightmost_index(items: list[int], target: int) -> int:  # => -1 if target is absent
    lo, hi = 0, len(items) - 1  # => the active search range
    result = -1  # => no match found yet
    while lo <= hi:  # => standard binary search bounds
        mid = (lo + hi) // 2  # => the midpoint of the active range
        if items[mid] == target:  # => found A match -- but is it the LAST one?
            result = mid  # => records this as the best-known rightmost match so far
            lo = mid + 1  # => keeps searching RIGHT for an even later occurrence
        elif (  # => opens the rightmost-side range-narrowing check
            items[mid] < target
        ):  # => same rule as leftmost -- target lies further right
            lo = mid + 1  # => shrinks the range from the left edge
        else:  # => same rule as leftmost -- target lies further left
            hi = mid - 1  # => shrinks the range from the right edge
    return result  # => the largest index where target occurs, or -1


data: list[int] = [1, 2, 2, 2, 3, 4, 4, 5]  # => sorted, with runs of duplicate values
print(leftmost_index(data, 2))  # => Output: 1 -- the first of three 2's
print(rightmost_index(data, 2))  # => Output: 3 -- the last of three 2's
print(leftmost_index(data, 4))  # => Output: 5
print(leftmost_index(data, 9))  # => Output: -1 -- 9 is absent entirely

assert leftmost_index(data, 2) == 1  # => confirms the first occurrence's index
assert rightmost_index(data, 2) == 3  # => confirms the last occurrence's index
assert leftmost_index(data, 9) == -1  # => confirms an absent target returns -1
assert rightmost_index(data, 9) == -1  # => confirms the mirrored absent case too
assert leftmost_index(data, 1) == rightmost_index(  # => a single-occurrence value
    data,  # => the same sorted array searched throughout
    1,  # => the value 1, which appears exactly once in data
)  # => a value with only ONE occurrence has matching leftmost and rightmost
print("ex-52 OK")  # => Output: ex-52 OK
