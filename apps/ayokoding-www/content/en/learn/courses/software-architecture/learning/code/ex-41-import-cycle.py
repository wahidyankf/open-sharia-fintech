# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 41: expose a two-module import cycle."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
graph = {"orders": {"payments"}, "payments": {"orders"}}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
has_cycle = "orders" in graph["payments"] and "payments" in graph["orders"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert has_cycle
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print("cycle found")
