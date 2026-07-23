"""Kata 3 (after): an explicit copy leaves the original untouched."""

original: list[int] = [1, 2, 3]
backup = original.copy()
backup.append(4)
print(original)
print(backup)
