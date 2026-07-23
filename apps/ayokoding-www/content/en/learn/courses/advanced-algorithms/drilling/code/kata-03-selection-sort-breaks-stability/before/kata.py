"""Kata 3 (before): a swap-based selection sort is unstable -- equal-key records lose their input order."""


def selection_sort_by_grade(students: list[tuple[int, str]]) -> list[tuple[int, str]]:
    arr = list(students)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j][0] < arr[min_idx][0]:
                min_idx = j
        arr[i], arr[min_idx] = (
            arr[min_idx],
            arr[i],
        )  # SMELL: a long-range swap can jump equal keys apart
    return arr


students = [(90, "alice"), (85, "bob"), (90, "carol"), (85, "dave")]
result = selection_sort_by_grade(students)
print(result)
# expected: alice before carol (both 90), bob before dave (both 85) -- their ORIGINAL relative order
print(result == [(85, "bob"), (85, "dave"), (90, "alice"), (90, "carol")])
