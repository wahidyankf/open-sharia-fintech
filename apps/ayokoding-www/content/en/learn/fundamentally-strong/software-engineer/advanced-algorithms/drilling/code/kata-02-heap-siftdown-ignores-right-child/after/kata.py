"""Kata 2 (after): sift-down compares BOTH children and picks the smaller one before swapping."""


def sift_down(heap: list[int], i: int, n: int) -> None:
    while True:
        left, right = 2 * i + 1, 2 * i + 2
        smallest = i
        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if (
            right < n and heap[right] < heap[smallest]
        ):  # => now genuinely considers the right child too
            smallest = right
        if smallest == i:
            break
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest


def heapify(arr: list[int]) -> list[int]:
    heap = list(arr)
    n = len(heap)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(heap, i, n)
    return heap


def is_min_heap(heap: list[int]) -> bool:
    n = len(heap)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and heap[i] > heap[left]:
            return False
        if right < n and heap[i] > heap[right]:
            return False
    return True


heap = heapify([5, 1, 9, 2, 8, 3, 0])
print(heap)
print(is_min_heap(heap))
