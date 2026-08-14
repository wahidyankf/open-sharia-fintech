"""Example 28: use a specification to select matching entities."""


def premium(spend: int) -> bool:
    return spend >= 100  # => the selection rule has a name


spends = [20, 100, 250]  # => sample domain values
matches = [
    spend for spend in spends if premium(spend)
]  # => callers pass the rule, not SQL text
assert matches == [100, 250]
print(matches)  # => Output: [100, 250]
