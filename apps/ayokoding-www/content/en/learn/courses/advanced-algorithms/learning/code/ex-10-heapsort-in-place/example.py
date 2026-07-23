"""Example 10: In-Place Heapsort via Manual Sift-Down."""

# Heapsort (co-09) builds a max-heap IN a plain list, then repeatedly swaps
# the max to the end and shrinks the heap -- O(n log n) time, O(1) extra
# space, unlike merge sort's O(n) auxiliary array.


def sift_down(items: list[int], start: int, end: int) -> None:  # => restores heap order
    root = start  # => the node that might need to sink down
    while True:  # => keeps sinking until root has no larger child, or no children left
        child = 2 * root + 1  # => index of root's LEFT child in the array encoding
        if child > end:  # => no children exist within the active heap range
            break  # => root is already in a valid position -- stop sifting
        if (  # => opens the two-part right-child-exists-and-is-bigger check
            child + 1 <= end and items[child + 1] > items[child]
        ):  # => right child bigger
            child += 1  # => picks the LARGER of the two children to compare against
        if items[root] >= items[child]:  # => root already beats both children
            break  # => the max-heap property holds here -- stop sifting
        items[root], items[child] = items[child], items[root]  # => sink root down
        root = child  # => continues sifting from the new position


def heapsort(items: list[int]) -> None:  # => sorts items IN PLACE, ascending
    n = len(items)  # => n = the number of elements to sort
    for start in range(  # => opens the bottom-up heap-build range
        n // 2 - 1,  # => the last non-leaf parent index
        -1,  # => stops just before index 0
        -1,  # => starts at the last non-leaf parent, walks toward the root
    ):  # => builds a max-heap bottom-up, O(n) total
        sift_down(items, start, n - 1)  # => fixes each subtree, from the last parent up
    for end in range(n - 1, 0, -1):  # => repeatedly extracts the current maximum
        items[0], items[end] = items[end], items[0]  # => moves max to its sorted slot
        sift_down(items, 0, end - 1)  # => restores heap order over the SHRUNK range


data: list[int] = [5, 13, 2, 25, 7, 17, 20, 8, 4]  # => 9 unsorted integers
heapsort(data)  # => sorts data IN PLACE -- no new list is allocated
print(data)  # => Output: [2, 4, 5, 7, 8, 13, 17, 20, 25]

assert data == [2, 4, 5, 7, 8, 13, 17, 20, 25]  # => confirms ascending sorted order
empty: list[int] = []  # => the empty-input edge case
heapsort(empty)  # => must not crash on an empty list
assert empty == []  # => confirms the empty list stays empty
print("ex-10 OK")  # => Output: ex-10 OK
