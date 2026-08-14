# => Keeps this domain step explicit and reviewable.
"""Example 28: use a specification to select matching entities."""


# => Names policy so callers do not recreate the rule.
def premium(spend: int) -> bool:
    return spend >= 100  # => the selection rule has a name


spends = [20, 100, 250]  # => sample domain values
# => Keeps scenario data close to the rule it exercises.
matches = [
    # => Keeps this domain step explicit and reviewable.
    spend
    # => Evaluates every candidate through one reusable business rule.
    for spend in spends
    # => Retains only values whose named policy is satisfied.
    if premium(spend)
]  # => callers pass the rule, not SQL text
# => Proves the stated business rule is observable.
assert matches == [100, 250]
print(matches)  # => Output: [100, 250]
