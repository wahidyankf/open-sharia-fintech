"""Example 67: invest modelling effort in a differentiating core."""

subdomains = {
    "pricing": "core",
    "catalog": "supporting",
    "email": "generic",
}  # => classification guides investment
assert (
    subdomains["pricing"] == "core"
)  # => pricing receives the richest model in this system
print("pricing is core")  # => Output: pricing is core
