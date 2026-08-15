# => Keeps this domain step explicit and reviewable.
"""Example 52: a boundary test forbids infrastructure imports."""

# => Keeps scenario data close to the rule it exercises.
domain_imports = [
    # => Keeps this domain step explicit and reviewable.
    "dataclasses",
    # => Keeps this domain step explicit and reviewable.
    "typing",
]  # => a sample domain module uses language facilities only
# => Keeps scenario data close to the rule it exercises.
forbidden = {
    # => Keeps this domain step explicit and reviewable.
    "sqlalchemy",
    # => Keeps this domain step explicit and reviewable.
    "requests",
    # => Keeps this domain step explicit and reviewable.
    "flask",
}  # => adapters, not domain rules, own these names
# => Proves the stated business rule is observable.
assert not forbidden.intersection(
    # => Keeps this domain step explicit and reviewable.
    domain_imports
)  # => an import test makes the direction executable
print("domain is isolated")  # => Output: domain is isolated
