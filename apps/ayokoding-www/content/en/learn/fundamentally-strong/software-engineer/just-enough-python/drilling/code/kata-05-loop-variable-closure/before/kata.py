"""Kata 5 (before): every lambda captures the SAME loop variable, by reference."""

makers = [lambda: i for i in range(3)]
print([m() for m in makers])
