"""Example 5: Top-Down Merge Sort -- Split, Recurse, Merge."""

# Divide-and-conquer (co-06): split the list in half, sort each half
# recursively, then MERGE the two sorted halves back together in O(n) (co-07).
import random  # => used only to build a randomized test input, not the algorithm


def merge_sort(items: list[int]) -> list[int]:  # => returns a NEW sorted list
    if len(items) <= 1:  # => base case: a list of 0 or 1 elements is already sorted
        return items  # => nothing to split or merge
    mid = len(items) // 2  # => the split point, roughly in half
    left = merge_sort(items[:mid])  # => recursively sort the left half
    right = merge_sort(items[mid:])  # => recursively sort the right half
    return merge(left, right)  # => combine two SORTED halves into one sorted list


def merge(left: list[int], right: list[int]) -> list[int]:  # => the O(n) combine step
    result: list[int] = []  # => accumulates the merged, sorted output
    i = j = 0  # => independent read cursors into left and right
    while i < len(left) and j < len(right):  # => walk both lists in lockstep
        if left[i] <= right[j]:  # => "<=" (not "<") keeps the merge stable (co-11)
            result.append(left[i])  # => the smaller-or-equal element wins this step
            i += 1  # => advances only the left cursor
        else:
            result.append(right[j])  # => right's element was strictly smaller
            j += 1  # => advances only the right cursor
    result.extend(left[i:])  # => appends whatever remains of left (already sorted)
    result.extend(right[j:])  # => appends whatever remains of right (already sorted)
    return result  # => a fully merged, sorted list


random.seed(42)  # => a fixed seed makes this "random" input reproducible
sample: list[int] = random.sample(range(1, 1000), 50)  # => 50 distinct random ints
sorted_sample = merge_sort(sample)  # => merge_sort's own answer
expected = sorted(sample)  # => Python's built-in Timsort, as the ground truth
print(sorted_sample == expected)  # => Output: True
print(sorted_sample[:5])  # => Output: the 5 smallest values, ascending

assert sorted_sample == expected  # => confirms merge_sort matches sorted() exactly
assert merge_sort([]) == []  # => confirms the empty-list edge case is handled
assert merge_sort([5]) == [5]  # => confirms the single-element edge case is handled
print("ex-05 OK")  # => Output: ex-05 OK
