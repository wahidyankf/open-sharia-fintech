"""Example 34: honor a fixture robots rule and rate budget."""

# => The local policy denies the private path before any extraction is attempted.
disallowed = {"/private"}
# => The small budget models polite request pacing for the authorized public path.
path, remaining_budget = "/public", 1
# => Proceed only when policy allows the path and a request token remains.
assert path not in disallowed and remaining_budget > 0
# => Output confirms the fixture request is both allowed and rate-budgeted.
print("robots respected; one request permitted")
