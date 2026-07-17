"""Kata 6 (before): backtracking violation -- a failed branch never undoes its choice before retrying."""


def find_subset(numbers: list[int], target: int) -> list[int] | None:
    chosen: list[int] = []

    def backtrack(index: int, remaining: int) -> bool:
        if remaining == 0:
            return True
        if index >= len(numbers) or remaining < 0:
            return False
        chosen.append(numbers[index])  # try INCLUDING this number
        if backtrack(index + 1, remaining - numbers[index]):
            return True
        # BUG: no chosen.pop() here -- the rejected number stays in `chosen` when we try EXCLUDING it
        return backtrack(index + 1, remaining)

    if backtrack(0, target):
        return chosen
    return None


result = find_subset([5, 3, 2], 2)
print(result)  # correct answer is [2] -- watch what the missing undo actually returns
