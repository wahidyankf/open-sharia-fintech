"""Example 33: add one allowlisted fixture header during interception."""

# => Start with ordinary request metadata that contains no sensitive credential.
headers = {"accept": "application/json"}
# => Add only the named test header approved by this local fixture contract.
headers["x-fixture-mode"] = "test"
# => Assert the injected value reached the request representation.
assert headers["x-fixture-mode"] == "test"
# => Output records the header name without printing a secret value.
print("header added: x-fixture-mode")
