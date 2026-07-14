"""Example 45: Bubble Sort."""


# Repeatedly swaps adjacent out-of-order pairs -- large values "bubble" to the end (co-16).
def bubble_sort(items: list[int]) -> list[int]:  # => a plain sorting function
    values = items.copy()  # => works on a copy so the caller's list is untouched
    n = len(values)  # => cached length, reused every outer pass
    for i in range(n):  # => after pass i, the LAST i elements are guaranteed sorted
        swapped = False  # => tracks whether this pass did any work at all
        for j in range(
            n - 1 - i
        ):  # => shrinks the unsorted range by one each outer pass
            if values[j] > values[j + 1]:  # => adjacent pair is out of order
                values[j], values[j + 1] = values[j + 1], values[j]  # => swap them
                swapped = True  # => records that this pass made progress
        if not swapped:  # => a pass with zero swaps means the list is already sorted
            break  # => early exit -- avoids wasted passes, still O(n^2) worst case
    return values  # => the fully sorted list


unsorted = [5, 2, 4, 6, 1, 3]  # => the same fixture as Examples 43-44
result = bubble_sort(unsorted)  # => large values bubble rightward each pass
print(result)  # => Output: [1, 2, 3, 4, 5, 6]

assert result == sorted(unsorted)  # => confirms the hand-rolled sort matches sorted()
print("ex-45 OK")  # => Output: ex-45 OK
