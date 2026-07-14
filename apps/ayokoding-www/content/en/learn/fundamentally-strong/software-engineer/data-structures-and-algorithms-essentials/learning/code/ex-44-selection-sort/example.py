"""Example 44: Selection Sort."""


# Repeatedly finds the minimum of the unsorted tail and swaps it forward -- O(n^2) (co-16).
def selection_sort(items: list[int]) -> list[int]:  # => a plain sorting function
    values = items.copy()  # => works on a copy so the caller's list is untouched
    for i in range(len(values)):  # => values[:i] is the growing sorted prefix
        min_index = (
            i  # => assume the current position holds the smallest remaining value
        )
        for j in range(i + 1, len(values)):  # => O(n) linear scan for the true minimum
            if values[j] < values[min_index]:  # => found a smaller candidate
                min_index = j  # => track its index for the swap below
        values[i], values[min_index] = (
            values[min_index],
            values[i],
        )  # => one swap per outer pass
    return values  # => the fully sorted list


unsorted = [5, 2, 4, 6, 1, 3]  # => the same fixture as Example 43
result = selection_sort(unsorted)  # => finds+places the minimum, n times over
print(result)  # => Output: [1, 2, 3, 4, 5, 6]

assert result == sorted(unsorted)  # => confirms the hand-rolled sort matches sorted()
print("ex-44 OK")  # => Output: ex-44 OK
