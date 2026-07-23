"""Kata 7 (after): materialize into a list to iterate it more than once."""

evens = [n for n in range(4) if n % 2 == 0]
total = sum(evens)
count = sum(1 for _ in evens)
print(total, count)
