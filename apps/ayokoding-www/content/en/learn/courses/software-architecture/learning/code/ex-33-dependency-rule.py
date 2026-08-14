"""Worked Example 33: keep framework packages out of a domain import set."""

domain_imports = {"orders.domain": {"typing", "decimal"}}
outer_packages = {"fastapi", "sqlalchemy"}
assert domain_imports["orders.domain"].isdisjoint(outer_packages)
print("dependency direction holds")
