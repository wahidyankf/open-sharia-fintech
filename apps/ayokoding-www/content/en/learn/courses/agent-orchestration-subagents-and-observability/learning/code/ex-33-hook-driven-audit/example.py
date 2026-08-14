# An audit record holds the tool and policy outcome.
audit: list[dict[str, str]] = []
# The hook records one minimal pre-call decision.
audit.append({"tool": "read", "decision": "allow"})
# The record supports later review without tool arguments.
assert audit[0]["decision"] == "allow"
# Print the audit event.
print(audit)
