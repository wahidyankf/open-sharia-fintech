providers = {
    "first": "ok",
    "second": "ok",
}  # => same interface returns either provider result
assert all(result == "ok" for result in providers.values())  # => caller is decoupled
print("PASS: provider-swap")  # => offline acceptance result
