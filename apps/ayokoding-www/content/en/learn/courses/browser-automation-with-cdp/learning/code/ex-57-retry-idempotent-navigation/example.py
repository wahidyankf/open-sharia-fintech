"""Example 57: retry a safe navigation, not an unsafe form submission."""

# => Navigation is modeled as an idempotent read-like operation on a fixture URL.
operation = {"name": "navigate", "idempotent": True}
# => A retry policy accepts only operations whose repeat has no duplicate side effect.
retry_allowed = operation["idempotent"]
# => The assertion rejects the temptation to use one retry rule for every action.
assert retry_allowed is True and operation["name"] == "navigate"
# => Output records why this operation may be retried.
print("retry allowed for navigation")
