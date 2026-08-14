"""Example 52: a boundary test forbids infrastructure imports."""

domain_imports = [
    "dataclasses",
    "typing",
]  # => a sample domain module uses language facilities only
forbidden = {
    "sqlalchemy",
    "requests",
    "flask",
}  # => adapters, not domain rules, own these names
assert not forbidden.intersection(
    domain_imports
)  # => an import test makes the direction executable
print("domain is isolated")  # => Output: domain is isolated
