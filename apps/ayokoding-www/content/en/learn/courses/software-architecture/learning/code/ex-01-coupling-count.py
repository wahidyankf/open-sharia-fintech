# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 1: count incoming and outgoing dependencies."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
dependencies = {"orders": {"payments", "catalog"}, "payments": set(), "catalog": set()}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
incoming = sum("orders" in targets for targets in dependencies.values())
# => This keeps the modeled rule explicit so its trade-off can be inspected.
outgoing = len(dependencies["orders"])
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print({"Ca": incoming, "Ce": outgoing})
