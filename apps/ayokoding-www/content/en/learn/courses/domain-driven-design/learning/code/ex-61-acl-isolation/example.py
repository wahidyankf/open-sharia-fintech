"""Example 61: isolation tests forbid a foreign model in domain types."""

domain_symbols = {
    "SalesCustomer",
    "CustomerId",
    "Money",
}  # => vocabulary owned by this context
foreign_symbols = {
    "LegacyCustomerDTO"
}  # => legacy transport types belong only in the ACL
assert domain_symbols.isdisjoint(
    foreign_symbols
)  # => context models do not import each other
print("isolated")  # => Output: isolated
