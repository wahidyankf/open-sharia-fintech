# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 2: calculate instability from coupling counts."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
ca, ce = 5, 1
# => This keeps the modeled rule explicit so its trade-off can be inspected.
instability = ce / (ca + ce)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(round(instability, 2))
