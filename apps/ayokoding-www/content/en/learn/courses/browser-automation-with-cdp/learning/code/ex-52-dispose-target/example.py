"""Example 52: dispose a target after completing its owned task."""

# => Target state begins allocated while the task is using browser capacity.
target = {"id": "target-1", "disposed": False}
# => Completion transitions the target to disposed instead of leaving it retained.
target["disposed"] = True
# => The assertion makes resource cleanup an observable completion condition.
assert target["disposed"] is True
# => Output records explicit target disposal.
print("target disposed")
