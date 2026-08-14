"""Example 63: apply an independent rate budget to a fixture origin."""

# => Each origin has its own remaining-token count rather than sharing a hidden global bucket.
budget = {"https://fixture.test": 1}
# => One authorized request consumes one token from that origin's budget.
budget["https://fixture.test"] -= 1
# => The assertion verifies the first request is accepted and leaves no extra capacity.
assert budget["https://fixture.test"] == 0
# => Output makes the per-origin policy observable.
print("fixture origin budget exhausted")
