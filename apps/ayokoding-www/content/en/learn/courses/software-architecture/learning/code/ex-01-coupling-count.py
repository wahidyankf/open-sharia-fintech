"""Worked Example 1: count incoming and outgoing dependencies."""

dependencies = {"orders": {"payments", "catalog"}, "payments": set(), "catalog": set()}
incoming = sum("orders" in targets for targets in dependencies.values())
outgoing = len(dependencies["orders"])
print({"Ca": incoming, "Ce": outgoing})
