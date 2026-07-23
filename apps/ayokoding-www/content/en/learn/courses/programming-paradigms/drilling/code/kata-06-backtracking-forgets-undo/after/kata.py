"""Kata 6 (after): backtracking fix -- a failed branch undoes (pops) its choice before trying the alternative."""


def find_subset(numbers: list[int], target: int) -> list[int] | None:
    chosen: list[int] = []

    def backtrack(index: int, remaining: int) -> bool:
        if remaining == 0:
            return True
        if index >= len(numbers) or remaining < 0:
            return False
        chosen.append(numbers[index])
        if backtrack(index + 1, remaining - numbers[index]):
            return True
        chosen.pop()  # undo the rejected choice BEFORE trying the "exclude this number" branch
        return backtrack(index + 1, remaining)

    if backtrack(0, target):
        return chosen
    return None


result = find_subset([5, 3, 2], 2)
print(result)
