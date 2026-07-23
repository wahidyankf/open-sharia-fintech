"""Example 46: Recursive Merge Sort."""


# Splits in half recursively, then merges sorted halves -- guaranteed O(n log n) (co-16, co-17).
def merge_sort(items: list[int]) -> list[int]:  # => the recursive driver
    if len(items) <= 1:  # => BASE CASE -- a list of 0 or 1 elements is already sorted
        return items  # => nothing to sort
    mid = len(items) // 2  # => splits the list into two roughly equal halves
    left = merge_sort(items[:mid])  # => RECURSIVE CASE: sort the left half
    right = merge_sort(items[mid:])  # => RECURSIVE CASE: sort the right half
    return _merge(left, right)  # => combine two SORTED halves into one sorted list


# Interleaves two sorted lists into one sorted list -- O(n) linear merge.
def _merge(left: list[int], right: list[int]) -> list[int]:  # => a merge helper
    merged: list[int] = []  # => the combined, sorted result
    i = j = 0  # => independent cursors into left and right
    while i < len(left) and j < len(
        right
    ):  # => picks the smaller front element each step
        if left[i] <= right[j]:  # => the left cursor's element is smaller-or-equal
            merged.append(left[i])  # => takes from the left side
            i += 1  # => advances the left cursor
        else:  # => the right cursor's element is smaller
            merged.append(right[j])  # => takes from the right side
            j += 1  # => advances the right cursor
    merged.extend(left[i:])  # => appends whichever side has leftovers -- already sorted
    merged.extend(right[j:])  # => appends any remaining right-side leftovers too
    return merged  # => the fully merged, sorted list


unsorted = [5, 2, 4, 6, 1, 3]  # => the same fixture as prior sorting examples
result = merge_sort(unsorted)  # => splits down to singletons, then merges back up
print(result)  # => Output: [1, 2, 3, 4, 5, 6]

assert result == sorted(unsorted)  # => confirms the hand-rolled sort matches sorted()
print("ex-46 OK")  # => Output: ex-46 OK
