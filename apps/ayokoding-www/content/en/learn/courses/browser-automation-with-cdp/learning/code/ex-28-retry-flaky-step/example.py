"""Example 28: retry one transient, idempotent fixture operation."""

# => The mutable attempt counter models one transient failure then a successful retry.
attempts = 0
# => Bound retries so a permanently broken operation cannot spin forever.
while attempts < 2:
    attempts += 1
    if attempts == 2:
        break
# => Success is explicit and occurs inside the fixed retry budget.
assert attempts == 2
# => Output documents the number of attempts used by the safe fixture.
print(f"completed on attempt {attempts}")
