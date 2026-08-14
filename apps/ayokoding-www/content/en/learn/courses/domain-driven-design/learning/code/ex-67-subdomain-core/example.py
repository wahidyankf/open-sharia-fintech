# => Keeps this domain step explicit and reviewable.
"""Example 67: invest modelling effort in a differentiating core."""

# => Keeps scenario data close to the rule it exercises.
subdomains = {
    # => Keeps this domain step explicit and reviewable.
    "pricing": "core",
    # => Keeps this domain step explicit and reviewable.
    "catalog": "supporting",
    # => Keeps this domain step explicit and reviewable.
    "email": "generic",
}  # => classification guides investment
# => Proves the stated business rule is observable.
assert (
    # => Keeps this domain step explicit and reviewable.
    subdomains["pricing"] == "core"
)  # => pricing receives the richest model in this system
print("pricing is core")  # => Output: pricing is core
