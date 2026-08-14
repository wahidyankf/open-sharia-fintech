"""Example 59: check fixture target health before assigning a job."""

# => The health probe exposes whether the target can safely accept work.
target = {"id": "target-1", "responsive": True}
# => Assignment is conditional on the probe instead of assuming a stale target is usable.
assignable = target["responsive"]
# => The assertion is the admission contract for the page pool.
assert assignable is True
# => Output identifies the target that passed the health check.
print(target["id"])
