"""Example 49: reclaim an unhealthy fixture worker before assigning work."""

# => One worker is stuck, while the replacement is explicitly healthy.
workers = [{"id": "old", "healthy": False}, {"id": "new", "healthy": True}]
# => Fleet selection chooses only a healthy worker after the failed one is reclaimed.
available = next(worker for worker in workers if worker["healthy"])
# => The task receives the replacement rather than silently using a dead worker.
assert available["id"] == "new"
# => Output records the recovered fleet assignment.
print("assigned healthy worker: new")
