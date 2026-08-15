outputs = {"provider-run-a": "yes", "provider-run-b": "yes"}  # => mock observations
assert set(outputs.values()) == {
    "yes"
}  # => fixture is stable, not a provider guarantee
print("PASS: temperature-zero")  # => offline acceptance result
