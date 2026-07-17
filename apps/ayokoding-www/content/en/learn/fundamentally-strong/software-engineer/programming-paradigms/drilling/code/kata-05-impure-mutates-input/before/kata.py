"""Kata 5 (before): purity violation -- a function that LOOKS pure secretly mutates its input."""


def sorted_scores(scores: list[int]) -> list[int]:
    scores.sort()  # BUG: list.sort() mutates IN PLACE -- the caller's list is silently changed too
    return scores


original = [3, 1, 2]
result = sorted_scores(original)
print(result)
print(original)  # SMELL: caller never asked for `original` to change, but it did
