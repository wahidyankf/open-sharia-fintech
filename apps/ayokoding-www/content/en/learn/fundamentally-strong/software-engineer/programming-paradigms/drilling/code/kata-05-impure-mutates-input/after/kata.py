"""Kata 5 (after): purity fix -- `sorted()` returns a NEW list, the caller's input is untouched."""


def sorted_scores(scores: list[int]) -> list[int]:
    return sorted(scores)  # pure -- builds and returns a new list, never touches the argument


original = [3, 1, 2]
result = sorted_scores(original)
print(result)
print(original)  # unchanged -- proves the function is referentially transparent
