"""Kata 1 (before): Lomuto partition forgets to swap the pivot into its final sorted position."""


def partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    return high  # BUG: never swaps arr[i + 1] with arr[high] -- the pivot never actually moves


def quicksort(arr: list[int], low: int, high: int) -> None:
    if low < high:
        p = partition(arr, low, high)
        quicksort(arr, low, p - 1)
        quicksort(arr, p + 1, high)


data = [5, 3, 8, 4, 2]
quicksort(data, 0, len(data) - 1)
print(data)
print(data == sorted([5, 3, 8, 4, 2]))
