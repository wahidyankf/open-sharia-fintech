"""Worked Example 30: identify an import of another module's internals."""

imports = {"orders.handlers": {"payments._vendor_client"}}
forbidden = any("._" in target for targets in imports.values() for target in targets)
assert forbidden
print("boundary violation found")
