"""Kata 7 (before): a generator can only be iterated once."""

evens = (n for n in range(4) if n % 2 == 0)
total = sum(evens)
count = sum(1 for _ in evens)
print(total, count)
