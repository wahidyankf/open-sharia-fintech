# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 33: keep framework packages out of a domain import set."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
domain_imports = {"orders.domain": {"typing", "decimal"}}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
outer_packages = {"fastapi", "sqlalchemy"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert domain_imports["orders.domain"].isdisjoint(outer_packages)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print("dependency direction holds")
