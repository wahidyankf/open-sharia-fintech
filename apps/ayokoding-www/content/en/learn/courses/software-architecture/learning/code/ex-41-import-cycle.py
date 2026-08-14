"""Worked Example 41: expose a two-module import cycle."""

graph = {"orders": {"payments"}, "payments": {"orders"}}
has_cycle = "orders" in graph["payments"] and "payments" in graph["orders"]
assert has_cycle
print("cycle found")
