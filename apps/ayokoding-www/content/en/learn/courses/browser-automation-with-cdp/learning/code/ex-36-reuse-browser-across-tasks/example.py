"""Example 36: reuse one fixture browser identity across tasks."""

# => One browser identifier represents a long-lived, pool-owned browser process.
browser = {"id": "browser-1", "launches": 1}
# => Independent tasks borrow the existing browser instead of launching replacements.
tasks = [{"browser": browser["id"]}, {"browser": browser["id"]}]
# => Both tasks share one browser while the launch count remains exactly one.
assert {task["browser"] for task in tasks} == {"browser-1"} and browser["launches"] == 1
# => Output proves the expensive browser lifecycle was reused.
print("one browser reused by two tasks")
