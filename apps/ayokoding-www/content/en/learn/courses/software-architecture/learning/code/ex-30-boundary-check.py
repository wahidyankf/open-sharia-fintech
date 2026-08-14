# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 30: identify an import of another module's internals."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
imports = {"orders.handlers": {"payments._vendor_client"}}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
forbidden = any("._" in target for targets in imports.values() for target in targets)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert forbidden
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print("boundary violation found")
