# A bounded attempt count prevents runaway retries.
attempts = 0
# The worker fails its only permitted attempt in this fixture.
attempts += 1
# Fallback follows the exhausted bounded policy.
result = "fallback" if attempts == 1 else "worker"
# The recovery path is deterministic and inspectable.
assert result == "fallback"
# Print the policy outcome.
print(result)
