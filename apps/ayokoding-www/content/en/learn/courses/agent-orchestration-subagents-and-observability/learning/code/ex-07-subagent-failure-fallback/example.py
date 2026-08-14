# A worker can report a typed failure.
def worker() -> str:
    # The local simulation avoids an external dependency.
    return "error"


# The parent owns the recovery decision.
result = "fallback-summary" if worker() == "error" else "worker-summary"
# Failure does not collapse the whole run.
assert result == "fallback-summary"
# Print the controlled fallback.
print(result)
