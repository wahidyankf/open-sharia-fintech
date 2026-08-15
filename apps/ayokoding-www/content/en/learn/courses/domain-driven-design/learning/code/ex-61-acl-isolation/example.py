# => Keeps this domain step explicit and reviewable.
"""Example 61: isolation tests forbid a foreign model in domain types."""

# => Keeps scenario data close to the rule it exercises.
domain_symbols = {
    # => Keeps this domain step explicit and reviewable.
    "SalesCustomer",
    # => Keeps this domain step explicit and reviewable.
    "CustomerId",
    # => Keeps this domain step explicit and reviewable.
    "Money",
}  # => vocabulary owned by this context
# => Keeps scenario data close to the rule it exercises.
foreign_symbols = {
    # => Keeps this domain step explicit and reviewable.
    "LegacyCustomerDTO"
}  # => legacy transport types belong only in the ACL
# => Proves the stated business rule is observable.
assert domain_symbols.isdisjoint(
    # => Keeps this domain step explicit and reviewable.
    foreign_symbols
)  # => context models do not import each other
print("isolated")  # => Output: isolated
