"""Example 47: Recursive Quicksort."""


# Partitions around a pivot, recurses on both sides -- O(n log n) average, but O(n^2)
# worst case with a poor pivot choice, e.g. an already-sorted input (co-16, co-17).
def quicksort(items: list[int]) -> list[int]:  # => the recursive driver
    if len(items) <= 1:  # => BASE CASE -- 0 or 1 elements are trivially sorted
        return items  # => nothing to sort
    pivot = items[len(items) // 2]  # => picks a middle element as the pivot
    less = [x for x in items if x < pivot]  # => everything strictly smaller than pivot
    equal = [
        x for x in items if x == pivot
    ]  # => every occurrence of the pivot value itself
    greater = [
        x for x in items if x > pivot
    ]  # => everything strictly larger than pivot
    return (
        quicksort(less) + equal + quicksort(greater)
    )  # => RECURSIVE CASE: sort each part


unsorted = [5, 2, 4, 6, 1, 3]  # => the same fixture as prior sorting examples
result = quicksort(
    unsorted
)  # => partitions around a pivot, then recurses on both sides
print(result)  # => Output: [1, 2, 3, 4, 5, 6]

assert result == sorted(unsorted)  # => confirms the hand-rolled sort matches sorted()
print("ex-47 OK")  # => Output: ex-47 OK
