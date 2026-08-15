"""Example 72: measure queue depth and active capacity at saturation."""

# => These metrics distinguish productive active work from callers waiting in a queue.
metrics = {"capacity": 2, "active": 2, "queued": 3}
# => Saturation means every slot is active while at least one request is waiting.
saturated = metrics["active"] == metrics["capacity"] and metrics["queued"] > 0
# => The assertion makes the operational threshold explicit and testable.
assert saturated is True
# => Output gives a compact capacity observation.
print(metrics)
