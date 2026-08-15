"""Example 60: reclaim a pool slot after a fixture task exceeds its deadline."""

# => The task state records that its deadline expired while it still held a slot.
task = {"id": "job-1", "timed_out": True, "slot_released": False}
# => Timeout handling releases capacity so waiting callers are not starved.
if task["timed_out"]:
    task["slot_released"] = True
# => The assertion verifies timeout and cleanup are one recovery operation.
assert task["slot_released"] is True
# => Output confirms the pool capacity was reclaimed.
print("stuck task reclaimed")
