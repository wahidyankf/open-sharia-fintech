"""Kata 5 (after): a default argument captures each i's VALUE at definition time."""

makers = [lambda i=i: i for i in range(3)]
print([m() for m in makers])
