"""Kata 3 (before): assignment aliases the same list object."""

original: list[int] = [1, 2, 3]
backup = original
backup.append(4)
print(original)
