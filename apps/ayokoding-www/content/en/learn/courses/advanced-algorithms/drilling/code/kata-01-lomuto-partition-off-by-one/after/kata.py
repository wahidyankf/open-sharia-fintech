"""Kata 1 (after): Lomuto partition swaps the pivot into its final sorted position before returning."""


def partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = (
        arr[high],
        arr[i + 1],
    )  # => the pivot moves to its correct sorted index
    return i + 1


def quicksort(arr: list[int], low: int, high: int) -> None:
    if low < high:
        p = partition(arr, low, high)
        quicksort(arr, low, p - 1)
        quicksort(arr, p + 1, high)


data = [5, 3, 8, 4, 2]
quicksort(data, 0, len(data) - 1)
print(data)
print(data == sorted([5, 3, 8, 4, 2]))
