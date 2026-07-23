"""Example 43: Insertion Sort."""


# Grows a sorted prefix one element at a time -- O(n^2) worst case (co-16).
def insertion_sort(items: list[int]) -> list[int]:  # => a plain sorting function
    values = items.copy()  # => works on a copy so the caller's list is untouched
    for i in range(1, len(values)):  # => values[:i] is already sorted at each step
        key = values[i]  # => the element being inserted into the sorted prefix
        j = i - 1  # => scans backward through the sorted prefix
        while j >= 0 and values[j] > key:  # => shifts larger elements one slot right
            values[j + 1] = values[j]  # => makes room for key
            j -= 1  # => continues scanning backward
        values[j + 1] = key  # => drops key into its now-correct position
    return values  # => the fully sorted list


unsorted = [5, 2, 4, 6, 1, 3]  # => a small unsorted list
result = insertion_sort(unsorted)  # => builds a sorted prefix left to right
print(result)  # => Output: [1, 2, 3, 4, 5, 6]

assert result == sorted(unsorted)  # => confirms the hand-rolled sort matches sorted()
print("ex-43 OK")  # => Output: ex-43 OK
