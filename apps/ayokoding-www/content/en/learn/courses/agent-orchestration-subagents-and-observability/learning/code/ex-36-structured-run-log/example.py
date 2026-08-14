# A log entry uses named fields for later queries.
entry = {"decision": "search", "tokens": 12, "outcome": "ok"}
# The record captures the required operational facts.
assert set(entry) == {"decision", "tokens", "outcome"}
# Print the structured log.
print(entry)
