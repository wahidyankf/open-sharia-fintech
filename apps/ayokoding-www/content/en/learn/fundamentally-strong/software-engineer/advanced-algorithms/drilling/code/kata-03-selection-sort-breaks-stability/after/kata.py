"""Kata 3 (after): Python's sorted() is stable -- equal-key records keep their original relative order."""


def stable_sort_by_grade(students: list[tuple[int, str]]) -> list[tuple[int, str]]:
    return sorted(
        students, key=lambda record: record[0]
    )  # => stable: never reorders equal-key pairs


students = [(90, "alice"), (85, "bob"), (90, "carol"), (85, "dave")]
result = stable_sort_by_grade(students)
print(result)
print(result == [(85, "bob"), (85, "dave"), (90, "alice"), (90, "carol")])
